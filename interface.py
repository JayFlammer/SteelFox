import tkinter as tk
from tkinter import ttk
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
        # Dateidialog, um mehrere IFC-Dateien auszuwählen
        file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
        if file_paths:
            # Speichere die Dateipfade in einer Instanzvariablen
            self.ifc_file_paths = list(file_paths)
            messagebox.showinfo("Information", f"{len(file_paths)} IFC-Datei(en) erfolgreich ausgewählt.")

            # Starte die Analyse direkt nach dem Upload
            self.analyze_reinforcement_data()
    
    def analyze_reinforcement_data(self):
        if not self.ifc_file_paths:
            messagebox.showwarning("Warnung", "Keine IFC-Dateien zum Analysieren ausgewählt.")
            return

        reinforcement_data = []

        # Iteriere über alle ausgewählten IFC-Dateien
        for file_path in self.ifc_file_paths:
            try:
                # IFC-Datei laden und Eigenschaften extrahieren
                model = load_ifc_data(file_path)
                data = reinforcement_extract_properties(model)

                if data:
                    reinforcement_data.extend(data)
                else:
                    messagebox.showinfo("Information", f"Keine Armierungseigenschaften im PropertySet 'HGL_B2F' in Datei '{file_path}' gefunden.")

            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der IFC-Datei '{file_path}': {str(e)}")

        if not reinforcement_data:
            messagebox.showinfo("Information", "Keine Armierungseigenschaften in den ausgewählten Dateien gefunden.")
            return

        # Neues Fenster für die Ausgabe erstellen, master verwenden
        output_window = tk.Toplevel(self.root)  # Statt tk.Toplevel(self)
        output_window.title("Armierungseigenschaften")

        # Rahmen für den Text und die Scrollbar erstellen
        frame = ttk.Frame(output_window)
        frame.pack(fill='both', expand=True)

        # Text-Widget erstellen, um die Ergebnisse zu zeigen
        text_widget = tk.Text(frame, wrap='word')
        text_widget.pack(side='left', fill='both', expand=True)

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget['yscrollcommand'] = scrollbar.set

        # Ergebnisse in das Text-Widget schreiben
        for data in reinforcement_data:
            text_widget.insert('end', f"Etappe: {data['Etappenbezeichnung']}\n")
            text_widget.insert('end', f"Material: {data['Material']}\n")
            text_widget.insert('end', f"Durchmesser: {data['Durchmesser']}\n")
            text_widget.insert('end', f"Gesamtgewicht: {data['Gesamtgewicht']} kg\n")
            text_widget.insert('end', f"Anzahl Eisen: {data['AnzahlEisen']}\n\n")

        # Text-Widget nur lesbar machen
        text_widget.config(state='disabled')



    def upload_new_reinforcement_ifc(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
        if file_path:
            messagebox.showinfo("Datei hochgeladen", "Armierung neu wurde erfolgreich hochgeladen.")
        else:
            messagebox.showerror("Fehler", "Keine Datei ausgewählt")