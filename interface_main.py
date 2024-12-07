import customtkinter as ctk
from tkinter import filedialog, messagebox

import json

from reinforcement_calculations import analyze_reinforcement_data

from interface.ui_main.frame_main import create_main_frame
from interface.ui_main.title_canvas import create_title_canvas
from interface.ui_main.logo_steelfox import add_steelfox_logo
from interface.ui_main.logo_halter import add_halter_logo
from interface.ui_main.title_steelfox import add_steelfox_text
from interface.ui_main.frame_input import create_input_frame
from interface.ui_main.frame_result import create_result_frame
from interface.ui_main.version_label import create_version_label

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd



class SteelFoxApp:
    
   

    def __init__(self, root):
            # Laden der Umgebungsvariablen
        load_dotenv()

        # Supabase-Zugangsdaten abrufen
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_API_KEY")

        # Supabase-Client erstellen
        if supabase_url and supabase_key:
            self.supabase: Client = create_client(supabase_url, supabase_key)
        else:
            raise Exception("SUPABASE_URL und SUPABASE_API_KEY sind erforderlich.")
        self.root = root
        self.root.title("SteelFox")
        self.root.geometry("1200x800")
        self.root.state('normal')
        self.root.resizable(True, True)

        # Event für den Vollbildmodus hinzufügen
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

        # Login-Daten laden
        self.login_data = self.load_login_data()

        # Titel-Canvas immer sichtbar machen
        self.title_canvas = create_title_canvas(self.root)
        self.title_canvas.pack(fill="x")
        add_steelfox_logo(self.title_canvas)
        add_steelfox_text(self.title_canvas)
        # Begrüßungstext in der Mitte des Titel-Canvas anzeigen
        self.welcome_label = ctk.CTkLabel(self.title_canvas, text="", font=("Helvetica", 16, "bold"), text_color="white")
        self.welcome_label.pack(side="top", pady=10, anchor="center")
        add_halter_logo(self.title_canvas)

        self.title_text = ""  # Anfangs leer

        self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')
        self.welcome_label.lift()

        # Start mit dem Anmeldeframe
        self.show_login_frame()

    def update_title_text(self, new_text):
        """Aktualisiert den Titeltext und das zugehörige Label."""
        self.title_text = new_text
        self.welcome_label.configure(text=self.title_text)

    def load_login_data(self):
        """Lädt die Login-Daten aus einer JSON-Datei."""
        try:
            with open("login_daten.json", "r") as file:
                data = json.load(file)
                return data.get("users", [])
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Die Datei 'login_daten.json' wurde nicht gefunden.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Fehler", "Die Datei 'login_daten.json' ist fehlerhaft.")
            return []

    def show_login_frame(self):
        """Zeigt das Anmeldeframe an"""
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.login_frame.pack(fill="both", expand=True)

        # Label und Eingabefelder
        ctk.CTkLabel(self.login_frame, text="Login", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self.login_frame, text="ID:", font=("Helvetica", 14)).pack(pady=5)
        self.id_entry = ctk.CTkEntry(self.login_frame)
        self.id_entry.pack(pady=5)

        ctk.CTkLabel(self.login_frame, text="Passwort:", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        # Enter-Taste für Login binden
        self.root.bind('<Return>', lambda event: self.check_login())

        # Login Button
        self.login_button = ctk.CTkButton(self.login_frame, text="Anmelden", command=self.check_login)
        self.login_button.pack(pady=20)

    def check_login(self):
        """Überprüft die Anmeldedaten"""
        user_id = self.id_entry.get()
        password = self.password_entry.get()

        # Überprüfen, ob ID und Passwort korrekt sind
        for user in self.login_data:
            if user['id'] == user_id and user['password'] == password:
                self.update_title_text(f"Willkommen zurück, {user_id}")
                self.show_selection_screen()  # Wechsel zum Auswahl-Screen
                return
        ctk.CTkLabel(self.login_frame, text="Ungültige Anmeldedaten", text_color="red").pack(pady=10)

    def show_selection_screen(self):
        """Zeigt einen schwarzen Screen mit Auswahlmöglichkeiten an"""
        # Altes Login-Frame entfernen
        if hasattr(self, "login_frame"):
            self.login_frame.pack_forget()
            self.login_frame.destroy()

        # Neues Frame für die Auswahl erstellen
        self.selection_frame = ctk.CTkFrame(self.root, fg_color="black")  # Schwarzer Hintergrund
        self.selection_frame.pack(fill="both", expand=True)

        # Auswahlmöglichkeiten hinzufügen
        label = ctk.CTkLabel(self.selection_frame, text="Bitte eine Option auswählen", font=("Helvetica", 16, "bold"), text_color="white")
        label.pack(pady=(50, 10))

        # Weißer Strich über den Buttons
        separator = ctk.CTkFrame(self.selection_frame, height=2, width=400, fg_color="white")
        separator.pack(pady=(0, 30))

        # Frame für die Optionen leicht oberhalb der Mitte des Bildschirms
        options_frame = ctk.CTkFrame(self.selection_frame, fg_color="black")
        options_frame.pack(pady=(0, 50))

        # Beispielbuttons für Optionen, alle gleich groß und nebeneinander in der Mitte
        button_width = 200
        button_height = 50

        create_project_button = ctk.CTkButton(options_frame, text="Neues Projekt erstellen", width=button_width, height=button_height, command=self.show_new_project_input, fg_color="#D2691E")
        create_project_button.grid(row=0, column=0, padx=20, pady=20)

        open_project_button = ctk.CTkButton(options_frame, text="Bestehendes Projekt öffnen", width=button_width, height=button_height, command=self.open_existing_project, fg_color="#D2691E")
        open_project_button.grid(row=0, column=1, padx=20, pady=20)

        compare_projects_button = ctk.CTkButton(options_frame, text="Mehrere Projekte vergleichen", width=button_width, height=button_height, command=self.compare_projects, fg_color="#D2691E")
        compare_projects_button.grid(row=0, column=2, padx=20, pady=20)

    def show_new_project_input(self):
        """Zeigt die Eingabefelder für ein neues Projekt innerhalb des aktuellen Frames an"""
        # Altes Auswahlframe entfernen
        if hasattr(self, "selection_frame"):
            self.selection_frame.pack_forget()
            self.selection_frame.destroy()
        
        # Neues Eingabe-Frame für Projektdetails erstellen
        self.project_input_frame = ctk.CTkFrame(self.root, fg_color="black")
        self.project_input_frame.pack(fill="both", expand=True)
        
        # Projektdetails Eingabefelder
        ctk.CTkLabel(self.project_input_frame, text="Projektnummer:", font=("Helvetica", 14), text_color="white").pack(pady=10)
        self.project_number_entry = ctk.CTkEntry(self.project_input_frame)
        self.project_number_entry.pack(pady=5)

        ctk.CTkLabel(self.project_input_frame, text="Projekt Name:", font=("Helvetica", 14), text_color="white").pack(pady=10)
        self.project_name_entry = ctk.CTkEntry(self.project_input_frame)
        self.project_name_entry.pack(pady=5)

        ctk.CTkLabel(self.project_input_frame, text="Projekt Kürzel:", font=("Helvetica", 14), text_color="white").pack(pady=10)
        self.project_short_entry = ctk.CTkEntry(self.project_input_frame)
        self.project_short_entry.pack(pady=5)

        ctk.CTkLabel(self.project_input_frame, text="Anzahl Etappen:", font=("Helvetica", 14), text_color="white").pack(pady=10)
        self.project_stages_entry = ctk.CTkEntry(self.project_input_frame)
        self.project_stages_entry.pack(pady=5)

        # Button zum Erstellen des Projekts
        create_button = ctk.CTkButton(self.project_input_frame, text="Projekt erstellen", command=self.create_project)
        create_button.pack(pady=20)

    def create_project(self):
        """Erstellt ein neues Projekt nach Validierung der Eingaben"""
        # Eingabewerte abrufen und als Instanzvariablen speichern
        self.project_number = self.project_number_entry.get()
        self.project_name = self.project_name_entry.get()
        self.project_short = self.project_short_entry.get()
        self.project_stages = self.project_stages_entry.get()

        # Eingabevalidierung
        if not self.project_number or not self.project_short:
            messagebox.showwarning("Eingabefehler", "Projektnummer und Projekt Kürzel müssen angegeben werden.")
            return

        if self.project_number == "0000":
            messagebox.showwarning("Eingabefehler", "Projektnummer '0000' ist ungültig.")
            return

        # Überprüfung, ob das Projekt bereits existiert (hier muss die Datenbankabfrage integriert werden)
        project_exists = self.check_project_exists(self.project_number, self.project_short)
        if project_exists == "both":
            messagebox.showerror("Fehler", "Dieses Projekt existiert bereits mit derselben Projektnummer und demselben Kürzel.")
            return
        elif project_exists == "short":
            messagebox.showwarning("Warnung", "Das Projektkürzel ist bereits vergeben. Bitte ein anderes Kürzel wählen.")
            return
        else:
            # Erstelle eine Datei mit project_number und project_short als Dateinamen
            project_filename = f"{self.project_number}_{self.project_short}.txt"
            
            try:
                # Erstelle die Datei im Projektordner
                with open(project_filename, 'w') as file:
                    file.write(f"Projektname: {self.project_name}\n")
                    file.write(f"Projektnummer: {self.project_number}\n")
                    file.write(f"Projektkürzel: {self.project_short}\n")
                    if self.project_stages:
                        file.write(f"Projektphasen: {self.project_stages}\n")

                # Merke dir das aktuell geöffnete Projekt als Dictionary
                self.current_project = {
                    "number": self.project_number,
                    "short": self.project_short,
                    "filename": project_filename
                }

                # Projektdaten in die Datenbank einfügen
                self.insert_project_data(self.project_number, self.project_name, self.project_short, self.project_stages)

                # Erfolgsmeldung
                messagebox.showinfo("Erfolg", f"Projekt '{self.project_name}' wurde erfolgreich erstellt.")
                
                # Schließe den aktuellen Eingabebereich und öffne das Hauptfenster
                self.project_input_frame.pack_forget()
                self.project_input_frame.destroy()
                self.show_main_frame()
            
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Erstellen der Projektdatei: {e}")

        # Die Rückgabe ist hier optional, da wir die Werte jetzt als Instanzvariablen haben.
        return self.project_number, self.project_name, self.project_short, self.project_stages



    
    def insert_project_data(self, project_number, project_name, project_short, project_stages):
        """Fügt ein neues Projekt in die Supabase-Datenbank ein"""
        try:
            # Die Anfrage an die Supabase-Datenbank senden
            response = self.supabase.table("projekte").insert({
                "projektnummer": project_number,
                "projekt_name": project_name,
                "projekt_kuerzel": project_short,
                "anzahl_etappen": project_stages
            }).execute()

            # Überprüfe den Status der Antwort
            if hasattr(response, 'status_code') and response.status_code >= 400:
                print(f"Fehler beim Einfügen der Projektdaten: Status-Code {response.status_code}")
                messagebox.showerror("Fehler", f"Das Projekt konnte nicht in die Datenbank hochgeladen werden. Fehlercode: {response.status_code}")
            elif hasattr(response, 'data') and response.data is None:
                print("Fehler beim Einfügen der Projektdaten: Keine Daten zurückgegeben.")
                messagebox.showerror("Fehler", "Das Projekt konnte nicht in die Datenbank hochgeladen werden. Keine Daten zurückgegeben.")
            else:
                print(f"Projektdaten erfolgreich eingefügt: {response.data}")
        except Exception as e:
            print("Hochgeladen")



    def check_project_exists(self, project_number, project_short):
        """Überprüft, ob ein Projekt mit der angegebenen Nummer und/oder Kürzel bereits existiert."""
        # Dieser Teil muss noch mit der Datenbanklogik ergänzt werden
        # Für das Beispiel: Angenommen, Projektnummer '1234' und Kürzel 'XYZ' sind bereits vorhanden
        if project_number == "1234" and project_short == "XYZ":
            return "both"
        elif project_short == "XYZ":
            return "short"
        return "none"

    def open_existing_project(self):
        """Logik zum Öffnen eines bestehenden Projekts"""
        # Hier könnte man einen Dateiauswahldialog hinzufügen
        file_paths = filedialog.askopenfilenames(filetypes=[("Projektdateien", "*.proj")])
        if file_paths:
            self.selection_frame.pack_forget()
            self.selection_frame.destroy()
            self.show_main_frame()  # Beispiel: Wechselt direkt zum Hauptframe

    def compare_projects(self):
        """Logik zum Vergleichen mehrerer Projekte"""
        # Hier könnte man mehrere Dateien zum Vergleich auswählen lassen
        file_paths = filedialog.askopenfilenames(filetypes=[("Projektdateien", "*.proj")])
        if file_paths:
            self.selection_frame.pack_forget()
            self.selection_frame.destroy()
            self.show_main_frame()  # Beispiel: Wechselt direkt zum Hauptframe

    def show_main_frame(self):
        """Zeigt das Hauptframe an"""
        # Neues Main Frame laden
        self.main_frame = create_main_frame(self.root)

        self.input_frame = create_input_frame(self.main_frame)
        self.result_frame = create_result_frame(self.main_frame)
        create_version_label(self.input_frame)  # Eingabebereich (linke Seite) - Unter dem Titelrahmen

        # Dateien Auswahl
        # Excel Armierung Alt
        self.xlsx_ausschreibung_label = ctk.CTkLabel(self.input_frame, text="Armierung Ausschreibung", font=("Helvetica", 14, "bold"), fg_color="#787575", text_color="#ffffff")
        self.xlsx_ausschreibung_label.pack(pady=5, padx=10, fill="x")

        self.xlsx_ausschreibung_button = ctk.CTkButton(self.input_frame, text="Excel Upload", command=self.upload_reinforcement_auschreibung, fg_color="#ffa8a8", text_color="white", width=200)
        self.xlsx_ausschreibung_button.pack(padx=10)

        self.xlsx_ausschreibung_count_label = ctk.CTkLabel(self.input_frame, text="Noch keine Datei hochgeladen", font=("Helvetica", 12), text_color="#ffffff")
        self.xlsx_ausschreibung_count_label.pack(padx=10, fill="x")

        # Eingabefeld für Datum der Unterzeichnung des Werkvertrags
        self.date_label = ctk.CTkLabel(self.input_frame, text="Datum der Unterzeichnung des Werkvertrags (TT.MM.JJJJ):", font=("Helvetica", 12), text_color="#ffffff")
        self.date_label.pack(pady=(10, 5), padx=10, fill="x")

        self.date_entry = ctk.CTkEntry(self.input_frame, placeholder_text="TT.MM.JJJJ", font=("Helvetica", 12), width=200)
        self.date_entry.pack(pady=5, padx=10)

        # IFC Armierung Ausführung
        self.ifc_ausfuehrung_label = ctk.CTkLabel(self.input_frame, text="Armierung Ausführung", font=("Helvetica", 14, "bold"), fg_color="#787575", text_color="#ffffff")
        self.ifc_ausfuehrung_label.pack(pady=10, padx=10, fill="x")

        self.ifc_ausfuehrung_button = ctk.CTkButton(self.input_frame, text="IFC Upload", command=self.upload_reinforcement_ausfuehrung, fg_color="#ffa8a8", text_color="white", width=200)
        self.ifc_ausfuehrung_button.pack(padx=10)

        self.ifc_ausfuehrung_count_label = ctk.CTkLabel(self.input_frame, text="Noch keine Datei hochgeladen", font=("Helvetica", 12), text_color="#ffffff")
        self.ifc_ausfuehrung_count_label.pack(padx=10, fill="x")

        # Button zur Analyse hinzufügen
        self.analyze_button = ctk.CTkButton(self.input_frame, text="Analyse starten", font=("Helvetica", 14), command=self.start_analysis, state='disabled', fg_color="#000000", text_color="white", width=200)
        self.analyze_button.pack(pady=20, padx=10)

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
            self.xlsx_ausschreibung_paths = list(file_paths)
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
        """Aktiviert den Analyse-Button, wenn alle Dateien (Excel und IFC) hochgeladen wurden."""
        if hasattr(self, 'ifc_ausfuehrung_paths') and self.ifc_ausfuehrung_paths and \
        hasattr(self, 'xlsx_ausschreibung_paths') and self.xlsx_ausschreibung_paths:
            self.analyze_button.configure(state='normal')

    def upload_excel_to_supabase(self, excel_file):
        """
        Liest eine Excel-Tabelle aus und lädt die Daten in eine Supabase-Tabelle hoch.
        
        :param excel_file: Pfad zur Excel-Datei
        """
        sheet_name = "Ausschreibung"  # Fester Tabellenblattname
        table_name = "tender_data_reinforcement"  # Fester Tabellenname für Supabase

        try:
            # Excel-Tabelle auslesen
            print(f"Lese Excel-Datei: {excel_file}, Blatt: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
            
            # Überprüfen, ob die benötigten Spalten existieren
            required_columns = {'NPK', 'Menge', 'Preis'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Die Excel-Datei muss die Spalten {required_columns} enthalten.")
            
            # Nur relevante Spalten auswählen und NaN-Werte entfernen
            df = df[['NPK', 'Menge', 'Preis']].dropna()
            print(f"Verarbeite {len(df)} Datensätze.")

            # Datum der Unterzeichnung aus dem Eingabefeld lesen
            contract_date = self.date_entry.get().strip()
            if not contract_date:
                raise ValueError("Das Datum der Unterzeichnung des Werkvertrags muss angegeben werden.")
            
            # Projektcode erstellen
            project_code = f"{self.project_number}_{self.project_short}"

            # Spaltennamen in DataFrame anpassen
            df.rename(columns={
                'Menge': 'menge',
                'Preis': 'preis'
            }, inplace=True)

            # Daten in ein Liste von Dictionaries umwandeln (Batch-Upload) und das Datum sowie Projektcode hinzufügen
            data = df.to_dict(orient='records')
            for record in data:
                record['datum'] = contract_date
                record['projekt_code'] = project_code

            # Daten auf Supabase hochladen
            print(f"Lade Daten in die Supabase-Tabelle '{table_name}' hoch...")
            response = self.supabase.table(table_name).insert(data).execute()

            if response.status_code == 201:
                print(f"{len(data)} Datensätze erfolgreich hochgeladen.")
            else:
                print(f"Fehler beim Hochladen: {response.data}")

        except FileNotFoundError as e:
            print(f"Die Datei wurde nicht gefunden: {e}")
        except ValueError as e:
            print(f"Fehler beim Verarbeiten der Excel-Datei: {e}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    def start_analysis(self):
        """
        Startet die Analyse und lädt relevante Daten in Supabase hoch.
        """
        try:
            # Prüfe, ob die Projektinformationen vorhanden sind
            if not hasattr(self, 'project_number') or not hasattr(self, 'project_short'):
                messagebox.showerror("Fehler", "Projektinformationen fehlen. Bitte erst ein Projekt erstellen.")
                return

            # Überprüfe, ob IFC-Dateien vorhanden sind
            if not hasattr(self, 'ifc_ausfuehrung_paths') or not self.ifc_ausfuehrung_paths:
                messagebox.showerror("Fehler", "IFC-Dateien fehlen. Bitte erst die Ausführungsdateien hochladen.")
                return

            # Übergabe des result_frame für die Ergebnisanzeige und der Projektinformationen
            analyze_reinforcement_data(self.ifc_ausfuehrung_paths, self.project_number, self.project_short)

            # Starte den Upload der Excel-Daten zu Supabase
            if hasattr(self, "xlsx_ausschreibung_paths") and self.xlsx_ausschreibung_paths:
                for excel_file in self.xlsx_ausschreibung_paths:
                    print(f"Starte Upload für Datei: {excel_file}")
                    self.upload_excel_to_supabase(excel_file)
            else:
                print("Keine Excel-Dateien zum Hochladen gefunden.")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Analyse oder beim Upload: {str(e)}")
