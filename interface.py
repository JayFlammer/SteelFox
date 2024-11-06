import tkinter as tk
from tkinter import filedialog, messagebox
from ifc_reader import load_ifc_data, concrete_extract_wall_slab_properties, reinforcement_extract_properties
from concrete_calculatons import calculate_concrete_volume

class SteelFoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SteelFox")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Haupt-Container Frame
        main_frame = tk.Frame(self.root, bg="#C0C0C0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo und Titel
        title_frame = tk.Frame(main_frame, bg="#606060", height=70)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        logo_label = tk.Label(title_frame, text="🦊 SteelFox", font=("Helvetica", 24, "bold"), fg="#FF8C00", bg="#606060")
        logo_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Eingabebereich (linke Seite)
        input_frame = tk.Frame(main_frame, bg="#D3D3D3", width=300)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        # IFC Dateien Auswahl
        self.ifc_new_label = tk.Label(input_frame, text="IFC Armierung Neu", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_new_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_new_button = tk.Button(input_frame, text=".ifc", command=self.upload_new_reinforcement_ifc)
        self.ifc_new_button.pack(anchor='w', padx=10)

        self.ifc_old_label = tk.Label(input_frame, text="IFC Armierung Alt", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_old_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_old_button = tk.Button(input_frame, text=".ifc", command=self.upload_old_reinforcement_ifc)
        self.ifc_old_button.pack(anchor='w', padx=10)

        self.ifc_concrete_label = tk.Label(input_frame, text="IFC Beton", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_concrete_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_concrete_button = tk.Button(input_frame, text=".ifc", command=self.upload_concrete_ifc)
        self.ifc_concrete_button.pack(anchor='w', padx=10)

        # Stahlpreis-Eingabefeld
        self.steel_price_label = tk.Label(input_frame, text="Stahlpreis", font=("Helvetica", 10), bg="#D3D3D3")
        self.steel_price_label.pack(pady=10, anchor='w', padx=10)
        self.steel_price_entry = tk.Entry(input_frame)
        self.steel_price_entry.pack(anchor='w', padx=10)

        # Hauptanzeige- / Ergebnisbereich (rechte Seite)
        result_frame = tk.Frame(main_frame, bg="#FFFFFF")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Versionshinweis
        version_label = tk.Label(main_frame, text="v1.1", font=("Helvetica", 8), bg="#D3D3D3")
        version_label.pack(side=tk.BOTTOM, anchor='e', padx=10, pady=5)

    def upload_concrete_ifc(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
        if file_path:
            try:
                # IFC-Datei laden und Daten extrahieren
                model = load_ifc_data(file_path)
                elements_data = concrete_extract_wall_slab_properties(model)
                # Betonmenge berechnen
                concrete_volume = calculate_concrete_volume(elements_data)
                messagebox.showinfo("Betonmenge", f"Die Betonmenge beträgt: {concrete_volume} m³")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Verarbeiten der IFC-Datei: {str(e)}")
        else:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt")

    def upload_old_reinforcement_ifc(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
        if file_path:
            try:
                # IFC-Datei laden und Armierungseigenschaften extrahieren
                model = load_ifc_data(file_path)
                reinforcement_data = reinforcement_extract_properties(model)

                # Prüfen, ob überhaupt Daten extrahiert wurden
                if not reinforcement_data:
                    messagebox.showinfo("Information", "Keine Armierungseigenschaften im PropertySet 'HGL_B2F' gefunden.")
                    return

                # Etappenbeziehungen berechnen und Materialien unterscheiden
                etappen_data = {}
                for data in reinforcement_data:
                    # Sicherstellen, dass `data` ein Dictionary ist
                    if isinstance(data, dict):
                        etappenbezeichnung = data.get("Etappenbezeichnung", "Unbekannte Etappe")
                        stahlgruppen_gewicht = data.get("Stabgruppe Gewicht", 0.0)
                        bauteilname = data.get("Bauteilname", "Unbekannt")

                        if etappenbezeichnung not in etappen_data:
                            etappen_data[etappenbezeichnung] = {
                                "Gesamtgewicht": 0.0,
                                "Materialien": {}
                            }

                        etappen_data[etappenbezeichnung]["Gesamtgewicht"] += stahlgruppen_gewicht

                        if bauteilname not in etappen_data[etappenbezeichnung]["Materialien"]:
                            etappen_data[etappenbezeichnung]["Materialien"][bauteilname] = 0.0
                        
                        etappen_data[etappenbezeichnung]["Materialien"][bauteilname] += stahlgruppen_gewicht

                # Ergebnisse anzeigen
                if etappen_data:
                    result_message = ""
                    for etappe, data in etappen_data.items():
                        result_message += f"Etappe: {etappe}\n"
                        result_message += f"  Gesamtgewicht: {data['Gesamtgewicht']} kg\n"
                        for material, gewicht in data["Materialien"].items():
                            result_message += f"  Material: {material}, Gewicht: {gewicht} kg\n"
                        result_message += "\n"

                    messagebox.showinfo("Armierungseigenschaften", result_message)
                else:
                    messagebox.showinfo("Information", "Keine passenden Etappenbeziehungen oder Materialdaten gefunden.")

            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Verarbeiten der IFC-Datei: {str(e)}")
        else:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt")


    def upload_new_reinforcement_ifc(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
        if file_path:
            messagebox.showinfo("Datei hochgeladen", "Armierung neu wurde erfolgreich hochgeladen.")
        else:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt")

