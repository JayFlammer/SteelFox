
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from steelfox_code.datas.ifc_reader import load_ifc_data
from steelfox_code.datas.concrete_extractor import concrete_extract_wall_slab_properties
from reinforcement_calculations import analyze_reinforcement_data

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

        # Haupt-Container Frame
        main_frame = tk.Frame(self.root, bg="#C0C0C0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas für den Titelbereich
        title_canvas = tk.Canvas(main_frame, bg="#606060", height=100, highlightthickness=0)
        title_canvas.pack(side=tk.TOP, fill=tk.X)

        # Logo Bild und Text-Label links
        try:
            # Pfad zum SteelFox Bild-Logo
            image_path = "Logo.png"  # Verwende den korrekten Pfad hier
            logo_image = Image.open(image_path)
            logo_image.thumbnail((70, 70), Image.LANCZOS)  # Seitenverhältnis beibehalten und die maximale Größe definieren
            logo_photo = ImageTk.PhotoImage(logo_image)

            # Bild-Label erstellen und im Canvas positionieren
            image_label = tk.Label(title_canvas, image=logo_photo, bg="#606060")
            image_label.image = logo_photo  # Referenz speichern, damit das Bild nicht vom Garbage Collector entfernt wird
            image_label.pack(side=tk.LEFT, padx=10, pady=10)

        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

        # Textlogo hinzufügen - links, direkt nach dem Bild
        logo_label = tk.Label(title_canvas, text="SteelFox", font=("Helvetica", 24, "bold"), fg="#FF8C00", bg="#606060")
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Halter-Logo rechts im Titelbereich hinzufügen
        try:
            # Pfad zum Halter Bild-Logo
            halter_logo_path = "Halter_Logo_Weiss_RGB.png"  # Verwende den korrekten Pfad hier
            halter_logo_image = Image.open(halter_logo_path)
            
            # Seitenverhältnis beibehalten und Größe anpassen
            max_width, max_height = 250, 120
            halter_logo_image.thumbnail((max_width, max_height), Image.LANCZOS)  # Halte Seitenverhältnis bei der Größenänderung
            halter_logo_photo = ImageTk.PhotoImage(halter_logo_image)

            # Bild-Label erstellen und im Canvas positionieren
            halter_image_label = tk.Label(title_canvas, image=halter_logo_photo, bg="#606060")
            halter_image_label.image = halter_logo_photo  # Referenz speichern, damit das Bild nicht vom Garbage Collector entfernt wird
            halter_image_label.pack(side=tk.RIGHT, padx=20, pady=10)

        except Exception as e:
            print(f"Fehler beim Laden des Halter Bildes: {e}")

        # Eingabebereich (linke Seite) - Unter dem Titelrahmen
        input_frame = tk.Frame(main_frame, bg="#D3D3D3", width=300)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(10, 0))

        # Hauptanzeige- / Ergebnisbereich (rechte Seite)
        result_frame = tk.Frame(main_frame, bg="#FFFFFF")
        result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # IFC Dateien Auswahl
        # IFC Armierung Neu
        self.ifc_new_label = tk.Label(input_frame, text="IFC Armierung Neu", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_new_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_new_button = tk.Button(input_frame, text="IFC Upload", command=self.upload_new_reinforcement_ifc, bg="#FF8C00", fg="white")
        self.ifc_new_button.pack(anchor='w', padx=10)
        self.ifc_new_count_label = tk.Label(input_frame, text="0 Dateien hochgeladen", font=("Helvetica", 8), bg="#D3D3D3")
        self.ifc_new_count_label.pack(anchor='w', padx=10)

        # IFC Armierung Alt
        self.ifc_old_label = tk.Label(input_frame, text="IFC Armierung Alt", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_old_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_old_button = tk.Button(input_frame, text="IFC Upload", command=self.upload_old_reinforcement_ifc, bg="#FF8C00", fg="white")
        self.ifc_old_button.pack(anchor='w', padx=10)
        self.ifc_old_count_label = tk.Label(input_frame, text="0 Dateien hochgeladen", font=("Helvetica", 8), bg="#D3D3D3")
        self.ifc_old_count_label.pack(anchor='w', padx=10)

        # IFC Beton
        self.ifc_concrete_label = tk.Label(input_frame, text="IFC Beton", font=("Helvetica", 10), bg="#D3D3D3")
        self.ifc_concrete_label.pack(pady=5, anchor='w', padx=10)
        self.ifc_concrete_button = tk.Button(input_frame, text="IFC Upload", command=self.upload_concrete_ifc, bg="#FF8C00", fg="white")
        self.ifc_concrete_button.pack(anchor='w', padx=10)
        self.ifc_concrete_count_label = tk.Label(input_frame, text="0 Datei hochgeladen", font=("Helvetica", 8), bg="#D3D3D3")
        self.ifc_concrete_count_label.pack(anchor='w', padx=10)

        # Button zur Analyse hinzufügen
        self.analyze_button = tk.Button(input_frame, text="Analyse starten", command=self.start_analysis, state='disabled')
        self.analyze_button.pack(pady=20, anchor='w', padx=10)

        # Versionshinweis - links unten platzieren
        version_label = tk.Label(input_frame, text="v1.1", font=("Helvetica", 8), bg="#D3D3D3")
        version_label.pack(side=tk.BOTTOM, anchor='w', padx=10, pady=5)

        # Variablen zur Speicherung der Dateipfade
        self.ifc_old_paths = []
        self.ifc_new_paths = []
        self.ifc_concrete_path = None

    def toggle_fullscreen(self, event=None):
        """Aktiviert/Deaktiviert den Vollbildmodus"""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        """Beendet den Vollbildmodus"""
        self.root.attributes("-fullscreen", False)

    def upload_concrete_ifc(self):
        file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
        if file_path:
            self.ifc_concrete_path = file_path
            # Button grün markieren und den Status aktualisieren
            self.ifc_concrete_button.config(bg="#32CD32", fg="white")
            self.ifc_concrete_count_label.config(text="1 Datei hochgeladen")
            self.check_all_files_uploaded()

    def upload_old_reinforcement_ifc(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
        if file_paths:
            self.ifc_old_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.ifc_old_button.config(bg="#32CD32", fg="white")
            self.ifc_old_count_label.config(text=f"{len(file_paths)} Datei(en) hochgeladen")
            self.check_all_files_uploaded()

    def upload_new_reinforcement_ifc(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
        if file_paths:
            self.ifc_new_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.ifc_new_button.config(bg="#32CD32", fg="white")
            self.ifc_new_count_label.config(text=f"{len(file_paths)} Datei(en) hochgeladen")
            self.check_all_files_uploaded()

    def check_all_files_uploaded(self):
        """Aktiviert den Analyse-Button, wenn alle Dateien hochgeladen wurden."""
        if self.ifc_old_paths and self.ifc_new_paths and self.ifc_concrete_path:
            self.analyze_button.config(state='normal')

    def start_analysis(self):
        try:
            # Hier die eigentliche Analyse durchführen
            analyze_reinforcement_data(self.ifc_old_paths + self.ifc_new_paths, self.root)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Analyse: {str(e)}")