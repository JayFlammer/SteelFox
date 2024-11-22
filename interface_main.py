import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from reinforcement_calculations import analyze_reinforcement_data

from interface.ui_Components.frame_main import create_main_frame
from interface.ui_Components.title_canvas import create_title_canvas
from interface.ui_Components.logo_steelfox import add_steelfox_logo
from interface.ui_Components.logo_halter import add_halter_logo
from interface.ui_Components.title_steelfox import add_steelfox_text
from interface.ui_Components.frame_input import create_input_frame
from interface.ui_Components.frame_result import create_result_frame
from interface.ui_Components.version_label import create_version_label

class SteelFoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SteelFox")
        self.root.geometry("1200x800")
        self.root.state('normal')
        self.root.resizable(True, True)

        # Event für den Vollbildmodus hinzufügen
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

        self.main_frame = create_main_frame(self.root)
        self.title_canvas = create_title_canvas(self.main_frame)

        add_steelfox_logo(self.title_canvas)
        add_steelfox_text(self.title_canvas)
        add_halter_logo(self.title_canvas)

        self.input_frame = create_input_frame(self.main_frame)
        self.result_frame = create_result_frame(self.main_frame)
        create_version_label(self.input_frame)# Eingabebereich (linke Seite) - Unter dem Titelrahmen



        # Dateien Auswahl
        # Excel Armierung Alt
        self.xlsx_ausschreibung_label = ctk.CTkLabel(self.input_frame, text="Armierung Ausschreibung", font=("Helvetica", 10, "bold"), fg_color="#787575", text_color="#ffffff")
        self.xlsx_ausschreibung_label.pack(pady=5, anchor='w', padx=10)
        self.xlsx_ausschreibung_button = ctk.CTkButton(self.input_frame, text="Excel Upload", command=self.upload_reinforcement_auschreibung, fg_color="#ffa8a8", text_color="white")
        self.xlsx_ausschreibung_button.pack(anchor='w', padx=10)
        self.xlsx_ausschreibung_count_label = ctk.CTkLabel(self.input_frame, text="Noch keine Datei hochgeladen", font=("Helvetica", 10), text_color="#ffffff")
        self.xlsx_ausschreibung_count_label.pack(anchor='w', padx=10)

        # IFC Armierung Ausführung
        self.ifc_ausfuehrung_label = ctk.CTkLabel(self.input_frame, text="Armierung Ausführung", font=("Helvetica", 10 , "bold"), fg_color="#787575", text_color="#ffffff")
        self.ifc_ausfuehrung_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_ausfuehrung_button = ctk.CTkButton(self.input_frame, text="IFC Upload", command=self.upload_reinforcement_ausfuehrung, fg_color="#ffa8a8", text_color="white")
        self.ifc_ausfuehrung_button.pack(anchor='w', padx=10)
        self.ifc_ausfuehrung_count_label = ctk.CTkLabel(self.input_frame, text="Noch keine Datei hochgeladen", font=("Helvetica", 10), text_color="#ffffff")
        self.ifc_ausfuehrung_count_label.pack(anchor='w', padx=10)
    

        # Button zur Analyse hinzufügen
        self.analyze_button = ctk.CTkButton(self.input_frame, text="Analyse starten", command=self.start_analysis, state='disabled', fg_color="#000000", text_color="white")
        self.analyze_button.pack(pady=20, anchor='w', padx=10)


        # Variablen zur Speicherung der Dateipfade
        self.ifc_old_paths = []
        self.ifc_new_paths = []

    def toggle_fullscreen(self, event=None):
        """Aktiviert/Deaktiviert den Vollbildmodus"""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        """Beendet den Vollbildmodus"""
        self.root.attributes("-fullscreen", False)


    def upload_reinforcement_auschreibung(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel file", "*.xlsx")])
        if file_paths:
            self.xlsx_auschreibung_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.xlsx_ausschreibung_button.configure(fg_color="#83fc83", text_color="white")
            self.xlsx_ausschreibung_count_label.configure(text=f"{len(file_paths)} Datei(en) hochgeladen")
            self.check_all_files_uploaded()

    def upload_reinforcement_ausfuehrung(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
        if file_paths:
            self.ifc_ausfuehrung_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.ifc_ausfuehrung_button.configure(fg_color="#83fc83", text_color="white")
            self.ifc_ausfuehrung_count_label.configure(text=f"{len(file_paths)} Datei(en) hochgeladen")
            self.check_all_files_uploaded()

    def check_all_files_uploaded(self):
        """Aktiviert den Analyse-Button, wenn alle Dateien hochgeladen wurden."""
        if self.ifc_ausfuehrung_paths:
            self.analyze_button.configure(state='normal')

    def start_analysis(self):
        try:
            # Übergabe des result_frame für die Ergebnisanzeige
            analyze_reinforcement_data(self.ifc_ausfuehrung_paths, self.result_frame)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Analyse: {str(e)}")

