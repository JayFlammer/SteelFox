from ifc_folder.ifc_file_handler import load_ifc_file
from ifc_folder.ifc_data_extractor import extract_concrete_volume, extract_reinforcement_count
from tkinter import messagebox
def calculate_cost(app):
    """
    Beispielhafte Funktion zur Berechnung der Kosten basierend auf den extrahierten Mengen.
    """
    if hasattr(app, 'concrete_file') and hasattr(app, 'old_reinforcement_file') and hasattr(app, 'new_reinforcement_file'):
        concrete_model = load_ifc_file(app.concrete_file)
        concrete_volume = extract_concrete_volume(concrete_model)

        old_reinforcement_model = load_ifc_file(app.old_reinforcement_file)
        new_reinforcement_model = load_ifc_file(app.new_reinforcement_file)

        old_reinforcement_count = extract_reinforcement_count(old_reinforcement_model)
        new_reinforcement_count = extract_reinforcement_count(new_reinforcement_model)

        # Beispielhafte Kostenberechnung
        cost_concrete = concrete_volume * 100  # Beispielpreis pro m^3 Beton
        cost_reinforcement_old = old_reinforcement_count * 10  # Beispielpreis pro Armierungselement
        cost_reinforcement_new = new_reinforcement_count * 10

        total_cost = cost_concrete + cost_reinforcement_old + cost_reinforcement_new

        messagebox.showinfo("Kosten berechnet", f"Gesamtkosten: {total_cost} CHF")
    else:
        messagebox.showerror("Fehler", "Bitte laden Sie zuerst alle benötigten Dateien hoch")
