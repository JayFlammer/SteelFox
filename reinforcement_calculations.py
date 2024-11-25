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
def insert_reinforcement_data(reinforcement_data):
    for data in reinforcement_data:
        try:
            response = supabase.table("reinforcement_data").insert({
                "listennummer": data.get("Listennummer", "Unbekannt"),
                "material": data.get("Material", "Unbekannt"),
                "durchmesser": data.get("Durchmesser", "Unbekannt"),
                "gesamtgewicht": data.get("Gesamtgewicht", 0.0)
            }).execute()
            
            if response.data:
                print(f"Daten erfolgreich eingefügt: {response.data}")
            else:
                print("Fehler beim Einfügen der Daten.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

# Funktion zur Analyse und Hochladen der Armierungsdaten
def analyze_reinforcement_data(ifc_file_paths):
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
                # Filtere die relevanten Daten aus dem PropertySet "HGL_B2F"
                filtered_data = []
                for element in data:
                    psets = element.get("PropertySets", {})
                    if "HGL_B2F" in psets:
                        listennummer = psets["HGL_B2F"].get("Listennummer", "Unbekannt")
                        durchmesser = psets["HGL_B2F"].get("Durchmesser", "Unbekannt")
                        gesamtgewicht = psets["HGL_B2F"].get("Stabgruppe Gewicht", 0.0)

                        element_data = {
                            "Listennummer": listennummer,
                            "Material": element.get("Material", "Unbekannt"),
                            "Durchmesser": durchmesser,
                            "Gesamtgewicht": gesamtgewicht
                        }
                        filtered_data.append(element_data)

                reinforcement_data.extend(filtered_data)
                print(f"Extrahierte Daten aus Datei '{file_path}': {len(filtered_data)} Elemente")
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei '{file_path}': {str(e)}")

    # Daten in die Datenbank hochladen
    if reinforcement_data:
        insert_reinforcement_data(reinforcement_data)
    else:
        print("Keine Armierungseigenschaften in den ausgewählten Dateien gefunden.")
