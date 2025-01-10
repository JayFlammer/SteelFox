from datas.reinforcement_extractor import extract_creation_date

from datas.ifc_reader import load_ifc_data
from datas.reinforcement_extractor import extract_all_reinforcement_properties
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Laden der Umgebungsvariablen
load_dotenv()

# Supabase-Zugangsdaten abrufen
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

# Supabase-Client erstellen
if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    raise Exception("SUPABASE_URL und SUPABASE_API_KEY sind erforderlich.")

# Daten aus reinforcement_data in Supabase-Datenbank einfügen
def insert_reinforcement_data(reinforcement_data, project_number, project_short, creation_date):
    """Fügt Armierungsdaten in die Datenbank ein, mit einem Projektcode basierend auf Projektnummer und Kürzel."""
    # Projektcode erstellen
    project_code = f"{project_number}{project_short}"

    # Durch die Armierungsdaten iterieren und sie in die Datenbank einfügen
    # Daten iterieren und sicherstellen, dass NPK ignoriert wird
    for data in reinforcement_data:
        # Entferne 'NPK', falls es vorhanden ist
        if "NPK" in data:
            del data["NPK"]
        
        try:
            # Daten in die Supabase-Datenbank einfügen
            response = supabase.table("reinforcement_data").insert({
                "listennummer": data.get("Listennummer", "Unbekannt"),
                "material": data.get("Material", "Unbekannt"),
                "durchmesser": data.get("Durchmesser", "Unbekannt"),
                "gesamtgewicht": data.get("Gesamtgewicht", 0.0),
                "etappe": data.get("Etappenbezeichnung", "Unbekannt"),
                "bearbeitungsgrad": data.get("Bearbeitungsgrad", "Unbekannt"),
                "projektcode": project_code,  # Projektcode hinzufügen
                "datum": creation_date  # Erstellungsdatum hinzufügen
            }).execute()
            
            if response.data:
                print(f"Daten erfolgreich eingefügt: {response.data}")
            else:
                print("Fehler beim Einfügen der Daten.")
        except Exception as e:
            print(f"Ein Fehler beim IFC ist aufgetreten: {e}")


def analyze_reinforcement_data(ifc_file_paths, project_number, project_short):
    """
    Analysiert Armierungsdaten aus den IFC-Dateien und lädt sie in die Datenbank.
    :param ifc_file_paths: Liste der Pfade zu den IFC-Dateien
    :param project_number: Projektnummer
    :param project_short: Projektkürzel
    """
    reinforcement_data = []

    # Iteriere über alle ausgewählten IFC-Dateien
    for file_path in ifc_file_paths:
        try:
            # IFC-Datei laden und Eigenschaften extrahieren
            model = load_ifc_data(file_path)
            if not model:
                print(f"Fehler beim Laden der Datei: {file_path}")
                continue

            # Extrahiere das Erstellungsdatum und andere Informationen aus der Datei
            file_info = extract_creation_date(file_path)
            creation_date = file_info

            print(creation_date)

            # Extrahiere die Armierungseigenschaften
            data = extract_all_reinforcement_properties(model)

            if data:
                # Filtere die relevanten Daten aus den PropertySets
                filtered_data = []
                for element in data:
                    psets = element.get("PropertySets", {})

                    # Eigenschaften aus "HGL_B2F" extrahieren
                    listennummer = psets.get("HGL_B2F", {}).get("Listennummer", "Unbekannt")
                    durchmesser = psets.get("HGL_B2F", {}).get("Durchmesser", "Unbekannt")
                    gesamtgewicht = psets.get("HGL_B2F", {}).get("Stabgruppe Gewicht", 0.0)
                    etappenbezeichnung = psets.get("HGL_B2F", {}).get("Etappenbezeichnung", "Unbekannt")

                    # Eigenschaften aus "Allplan_ReinforcingBar" extrahieren
                    bearbeitungsgrad = psets.get("Allplan_ReinforcingBar", {}).get("Shape code", "Unbekannt")

                    # Zusammenstellen der extrahierten Daten
                    element_data = {
                        "Listennummer": listennummer,
                        "Material": element.get("Material", "Unbekannt"),
                        "Durchmesser": durchmesser,
                        "Gesamtgewicht": gesamtgewicht,
                        "Etappenbezeichnung": etappenbezeichnung,
                        "Bearbeitungsgrad": bearbeitungsgrad
                    }
                    filtered_data.append(element_data)

                reinforcement_data.extend(filtered_data)
                print(f"Extrahierte Daten aus Datei '{file_path}': {len(filtered_data)} Elemente")

            # Daten in die Datenbank hochladen für die aktuelle Datei
            if filtered_data:
                insert_reinforcement_data(filtered_data, project_number, project_short, creation_date)

        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei '{file_path}': {str(e)}")