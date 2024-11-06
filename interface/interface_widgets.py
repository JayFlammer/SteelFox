import tkinter as tk
from tkinter import filedialog, messagebox
from ifc_manager.ifc_file_handler import read_ifc_data
from ifc_manager.ifc_element_extractor import extract_concrete_and_reinforcement

def create_widgets(app):
    # Upload-Felder für Armierung alt, Armierung neu und Betongehalt
    app.upload_label_old_reinforcement = tk.Label(app.root, text="Armierung alt hochladen")
    app.upload_label_old_reinforcement.pack(pady=5)
    app.upload_button_old_reinforcement = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_files(app, 'old_reinforcement'))
    app.upload_button_old_reinforcement.pack(pady=5)

    app.upload_label_new_reinforcement = tk.Label(app.root, text="Armierung neu hochladen")
    app.upload_label_new_reinforcement.pack(pady=5)
    app.upload_button_new_reinforcement = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_files(app, 'new_reinforcement'))
    app.upload_button_new_reinforcement.pack(pady=5)

    app.upload_label_concrete = tk.Label(app.root, text="Betongehalt hochladen")
    app.upload_label_concrete.pack(pady=5)
    app.upload_button_concrete = tk.Button(app.root, text="Dateien auswählen", command=lambda: load_files(app, 'concrete'))
    app.upload_button_concrete.pack(pady=5)

    # Button zum Anzeigen der extrahierten Daten (nur als Beispiel)
    app.extract_button = tk.Button(app.root, text="Extrahiere Daten", command=lambda: extract_data(app))
    app.extract_button.pack(pady=10)

def load_files(app, category):
    file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
    if file_paths:
        if category == 'old_reinforcement':
            app.old_reinforcement_files = file_paths
        elif category == 'new_reinforcement':
            app.new_reinforcement_files = file_paths
        elif category == 'concrete':
            app.concrete_files = file_paths
    else:
        messagebox.showerror("Fehler", "Keine Dateien ausgewählt")

def extract_data(app):
    if hasattr(app, 'old_reinforcement_files') and hasattr(app, 'new_reinforcement_files') and hasattr(app, 'concrete_files'):
        # Beispiel für das Verarbeiten der Dateien - hier könnte man die IFC-Daten einlesen und weiterverarbeiten
        for file_path in app.old_reinforcement_files:
            model = read_ifc_data(file_path)
            concrete, reinforcement = extract_concrete_and_reinforcement(model)
            messagebox.showinfo("Daten extrahiert", f"Datei: {file_path}\nBeton: {len(concrete)} Elemente, Armierung: {len(reinforcement)} Elemente")
    else:
        messagebox.showerror("Fehler", "Bitte laden Sie zuerst alle benötigten Dateien hoch")