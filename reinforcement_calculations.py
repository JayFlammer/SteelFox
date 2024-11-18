from tkinter import ttk
import tkinter as tk
from tkinter import messagebox


from steelfox_code.datas.ifc_reader import load_ifc_data
from steelfox_code.datas.reinforcement_extractor import reinforcement_extract_properties

def analyze_reinforcement_data(ifc_file_paths, root):
    if not ifc_file_paths:
        messagebox.showwarning("Warnung", "Keine IFC-Dateien zum Analysieren ausgewählt.")
        return

    reinforcement_data = []

    # Iteriere über alle ausgewählten IFC-Dateien
    for file_path in ifc_file_paths:
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

    # Neues Fenster für die Ausgabe erstellen
    output_window = tk.Toplevel(root)  # Verwende `root` anstelle von `self`
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