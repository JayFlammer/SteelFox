import tkinter as tk
from tkinter import filedialog, messagebox
from ifc_folder.ifc_file_handler import load_ifc_file
from ifc_folder.ifc_data_extractor import extract_concrete_volume, extract_reinforcement_count
from calculation_folder.cost_calculator import calculate_cost

def create_widgets(app):
    print("Widgets werden erstellt")
    # Upload-Felder für Armierung alt, Armierung neu und Betongehalt
    app.upload_label_old_reinforcement = tk.Label(app.root, text="Armierung alt hochladen")
    app.upload_label_old_reinforcement.pack(pady=5)
    app.upload_button_old_reinforcement = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_file(app, 'old_reinforcement'))
    app.upload_button_old_reinforcement.pack(pady=5)

    app.upload_label_new_reinforcement = tk.Label(app.root, text="Armierung neu hochladen")
    app.upload_label_new_reinforcement.pack(pady=5)
    app.upload_button_new_reinforcement = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_file(app, 'new_reinforcement'))
    app.upload_button_new_reinforcement.pack(pady=5)

    app.upload_label_concrete = tk.Label(app.root, text="Betongehalt hochladen")
    app.upload_label_concrete.pack(pady=5)
    app.upload_button_concrete = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_file(app, 'concrete'))
    app.upload_button_concrete.pack(pady=5)

    # Button zum Anzeigen der extrahierten Daten
    app.extract_button = tk.Button(app.root, text="Extrahiere Daten", command=lambda: extract_data(app))
    app.extract_button.pack(pady=10)

    # Button zur Kostenkalkulation
    app.calculate_cost_button = tk.Button(app.root, text="Kosten berechnen", command=lambda: calculate_cost(app))
    app.calculate_cost_button.pack(pady=10)

def load_file(app, category):
    file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if file_path:
        if category == 'old_reinforcement':
            app.old_reinforcement_file = file_path
        elif category == 'new_reinforcement':
            app.new_reinforcement_file = file_path
        elif category == 'concrete':
            app.concrete_file = file_path
    else:
        messagebox.showerror("Fehler", "Keine Datei ausgewählt")

def extract_data(app):
    if hasattr(app, 'old_reinforcement_file') and hasattr(app, 'new_reinforcement_file') and hasattr(app, 'concrete_file'):
        # Extraktion der Betonmenge
        concrete_model = load_ifc_file(app.concrete_file)
        concrete_volume = extract_concrete_volume(concrete_model)

        # Extraktion der Armierungsmengen
        old_reinforcement_model = load_ifc_file(app.old_reinforcement_file)
        new_reinforcement_model = load_ifc_file(app.new_reinforcement_file)

        old_reinforcement_count = extract_reinforcement_count(old_reinforcement_model)
        new_reinforcement_count = extract_reinforcement_count(new_reinforcement_model)

        # Anzeige der Ergebnisse
        messagebox.showinfo("Daten extrahiert", f"Betonmenge: {concrete_volume} m^3\nArmierung alt: {old_reinforcement_count} Elemente\nArmierung neu: {new_reinforcement_count} Elemente")
    else:
        messagebox.showerror("Fehler", "Bitte laden Sie zuerst alle benötigten Dateien hoch")