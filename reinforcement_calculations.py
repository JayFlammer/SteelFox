import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

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
def insert_reinforcement_data(reinforcement_data, project_number, project_short):
    """Fügt Armierungsdaten in die Datenbank ein, mit einem Projektcode basierend auf Projektnummer und Kürzel."""
    # Projektcode erstellen
    project_code = f"{project_number}_{project_short}"

    # Durch die Armierungsdaten iterieren und sie in die Datenbank einfügen
    for data in reinforcement_data:
        try:
            # Füge den Projektcode zum Datensatz hinzu
            response = supabase.table("reinforcement_data").insert({
                "listennummer": data.get("Listennummer", "Unbekannt"),
                "material": data.get("Material", "Unbekannt"),
                "durchmesser": data.get("Durchmesser", "Unbekannt"),
                "gesamtgewicht": data.get("Gesamtgewicht", 0.0),
                "etappe": data.get("Etappenbezeichnung", "Unbekannt"),
                "bearbeitungsgrad": data.get("Bearbeitungsgrad", "Unbekannt"),
                "projektcode": project_code  # Projektcode hinzufügen
            }).execute()
            
            if response.data:
                print(f"Daten erfolgreich eingefügt: {response.data}")
            else:
                print("Fehler beim Einfügen der Daten.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

def analyze_reinforcement_data(ifc_file_paths, project_number, project_short):
    reinforcement_data = []

    # Iteriere über alle ausgewählten IFC-Dateien
    for file_path in ifc_file_paths:
        try:
            # IFC-Datei laden und Eigenschaften extrahieren
            model = load_ifc_data(file_path)
            if not model:
                print(f"Fehler beim Laden der Datei: {file_path}")
                continue

            data = extract_all_reinforcement_properties(model)

            if data:
                # Filtere die relevanten Daten aus dem PropertySet "HGL_B2F" und "Allplan_ReinforcingBar"
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
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei '{file_path}': {str(e)}")

    # Daten in die Datenbank hochladen
    if reinforcement_data:
        # Hier werden nun auch die Projektnummer und das Kürzel übergeben
        insert_reinforcement_data(reinforcement_data, project_number, project_short)
    else:
        print("Keine Armierungseigenschaften in den ausgewählten Dateien gefunden.")
