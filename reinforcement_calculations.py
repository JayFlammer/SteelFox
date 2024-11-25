import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from datas.ifc_reader import load_ifc_data
from datas.reinforcement_extractor import extract_all_reinforcement_properties

def analyze_reinforcement_data(ifc_file_paths, result_frame):
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
            else:
                messagebox.showinfo("Information", f"Keine Armierungseigenschaften im PropertySet 'HGL_B2F' in Datei '{file_path}' gefunden.")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der IFC-Datei '{file_path}': {str(e)}")

    if not reinforcement_data:
        messagebox.showinfo("Information", "Keine Armierungseigenschaften in den ausgewählten Dateien gefunden.")
        return

    print(f"Anzahl der gesamten extrahierten Armierungselemente: {len(reinforcement_data)}")

    # Lösche den Inhalt des Ergebnisrahmens, um Platz für neue Ergebnisse zu schaffen
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Rahmen für den Text und die Scrollbar erstellen
    frame = ctk.CTkFrame(result_frame)
    frame.pack(fill='both', expand=True)

    # Text-Widget erstellen, um die Ergebnisse zu zeigen
    text_widget = ctk.CTkTextbox(frame, wrap='word')
    text_widget.pack(side='left', fill='both', expand=True)

    # Scrollbar hinzufügen
    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    text_widget['yscrollcommand'] = scrollbar.set

    # Ergebnisse in das Text-Widget schreiben
    for data in reinforcement_data:
        text_widget.insert('end', f"Listennummer: {data.get('Listennummer', 'Unbekannt')}\n")
        text_widget.insert('end', f"Material: {data.get('Material', 'Unbekannt')}\n")
        text_widget.insert('end', f"Durchmesser: {data.get('Durchmesser', 'Unbekannt')}\n")
        text_widget.insert('end', f"Gesamtgewicht: {data.get('Gesamtgewicht', 0.0)} kg\n")
        text_widget.insert('end', "\n")



    # Text-Widget nur lesbar machen
    text_widget.configure(state='disabled')


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

# Beispiel für das Einfügen der Daten
reinforcement_data = [
    {
        "Listennummer": "123",
        "Material": "Stahl",
        "Durchmesser": "12mm",
        "Gesamtgewicht": 150.5
    },
    {
        "Listennummer": "124",
        "Material": "Edelstahl",
        "Durchmesser": "10mm",
        "Gesamtgewicht": 120.0
    }
]

insert_reinforcement_data(reinforcement_data)
