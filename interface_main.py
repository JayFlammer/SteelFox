import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import json
import datetime

from datas.reinforcement_calculations import analyze_reinforcement_data

from interface.ui_main.frame_main import create_main_frame
from interface.canvas.title_canvas import create_title_canvas
from interface.canvas.logo_steelfox import add_steelfox_logo
from interface.canvas.logo_halter import add_halter_logo
from interface.canvas.title_steelfox import add_steelfox_text
from interface.ui_main.frame_input import create_input_frame
from interface.ui_main.frame_result import create_result_frame
from interface.canvas.version_label import create_version_label

import os
from supabase import create_client, Client
from dotenv import load_dotenv

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    
    def add_logout_button(self, parent_frame):
        """
        Fügt einen Logout-Button zu einem bestimmten Frame hinzu.

        Parameter:
            parent_frame (ctk.CTkFrame): Das Frame, in dem der Button platziert wird.
        """
        logout_button = ctk.CTkButton(parent_frame, text="Logout", command=self.show_login_frame, fg_color="red", text_color="black")
        logout_button.pack(side="bottom", pady=20)

    def add_leave_project_button(self, parent_frame):
        """
        Fügt einen 'Projekt verlassen'-Button zu einem bestimmten Frame hinzu.

        Parameter:
            parent_frame (ctk.CTkFrame): Das Frame, in dem der Button platziert wird.
        """
        leave_project_button = ctk.CTkButton(parent_frame, text="Projekt verlassen", command=self.show_selection_screen, fg_color="#ffa500", text_color="black")
        leave_project_button.pack(side="bottom", pady=20)

    def add_logout_button_and_leave_project_button(self, parent_frame):
        """
        Fügt die Buttons 'Logout' und 'Projekt verlassen' nebeneinander zu einem Frame hinzu.

        Parameter:
            parent_frame (ctk.CTkFrame): Das Frame, in dem die Buttons platziert werden.
        """
        # Erstelle einen Container-Frame für die Buttons
        button_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        button_frame.pack(side="bottom", pady=20)

        # 'Projekt verlassen'-Button hinzufügen
        leave_project_button = ctk.CTkButton(button_frame, text="Projekt verlassen", command=self.show_selection_screen, fg_color="#ffa500", text_color="black")
        leave_project_button.pack(side="left", padx=10)  # 'left' sorgt dafür, dass die Buttons nebeneinander erscheinen

        # Logout-Button hinzufügen
        logout_button = ctk.CTkButton(button_frame, text="Logout", command=self.show_login_frame, fg_color="red", text_color="black")
        logout_button.pack(side="left", padx=10)


    def load_login_data(self):
        """
        Lädt die Login-Daten aus einer JSON-Datei.

        Rückgabe:
            list: Eine Liste mit Benutzerinformationen aus der Datei.
        """
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
        """
        Zeigt das Anmeldefenster an.
        """
        # Entferne das aktuelle Frame, falls vorhanden
        self.clear_frames()

        # Neues Login-Frame erstellen
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

        # Login Button
        self.login_button = ctk.CTkButton(self.login_frame, text="Anmelden", command=self.check_login)
        self.login_button.pack(pady=20)

    def check_login(self):
        """
        Überprüft die eingegebenen Login-Daten und meldet den Benutzer an, falls diese korrekt sind.
        """
        user_id = self.id_entry.get()
        password = self.password_entry.get()

        # Überprüfen, ob ID und Passwort korrekt sind
        for user in self.login_data:
            if user['id'] == user_id and user['password'] == password:
                self.update_title_text(f"Willkommen zurück, {user_id}")
                self.show_selection_screen()  # Wechsel zum Auswahl-Screen
                return
        ctk.CTkLabel(self.login_frame, text="Ungültige Anmeldedaten", text_color="red").pack(pady=10)

    def update_title_text(self, new_text):
        """
        Aktualisiert den Titeltext in der Benutzeroberfläche.

        Parameter:
            new_text (str): Der neue Titeltext.
        """
        self.title_text = new_text
        self.welcome_label.configure(text=self.title_text)

    def show_selection_screen(self):
        """
        Zeigt das Auswahlmenü für den Benutzer nach erfolgreichem Login.
        """
        # Altes Login-Frame entfernen
        self.clear_frames()

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
        
        self.add_logout_button(self.selection_frame)
    
    def show_project_search_frame(self):
        """
        Zeigt das UI-Frame für die Projektsuche an.
        """
        # Altes Auswahlframe entfernen
        if hasattr(self, "selection_frame"):
            self.selection_frame.pack_forget()
            self.selection_frame.destroy()
        

        # Neues Frame für Projektsuche erstellen
        self.project_search_frame = ctk.CTkFrame(self.root, fg_color="black")
        self.project_search_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.project_search_frame, text="Projektsuche", font=("Helvetica", 20, "bold"), text_color="white").pack(pady=20)

        ctk.CTkLabel(self.project_search_frame, text="Projektnummer:", font=("Helvetica", 14), text_color="white").pack(pady=5)
        self.project_number_entry = ctk.CTkEntry(self.project_search_frame)
        self.project_number_entry.pack(pady=5)

        ctk.CTkLabel(self.project_search_frame, text="Projekt Kürzel:", font=("Helvetica", 14), text_color="white").pack(pady=5)
        self.project_short_entry = ctk.CTkEntry(self.project_search_frame)
        self.project_short_entry.pack(pady=5)

        search_button = ctk.CTkButton(self.project_search_frame, text="Projekt suchen", command=self.search_project, fg_color="#ffa500")
        search_button.pack(pady=20)

        self.add_logout_button_and_leave_project_button(self.project_search_frame)

    def search_project(self):
        """
        Sucht in der Datenbank nach einem Projekt mit der eingegebenen Projektnummer und dem Kürzel.

        Rückgabe:
            tuple: (Projektnummer, Projektkürzel) falls gefunden, sonst None.
        """
        self.project_number = self.project_number_entry.get().strip()
        self.project_short = self.project_short_entry.get().strip()

        if not self.project_number or not self.project_short:
            messagebox.showerror("Fehler", "Bitte sowohl Projektnummer als auch Projekt Kürzel angeben.")
            return

        project_code = f"{self.project_number}{self.project_short}"

        try:
            # Suche in der Datenbank nach dem Projektcode
            response = self.supabase.table("projekte").select("*").filter("projekt_code", "eq", project_code).execute()

            if response.data:  # Wenn das Projekt existiert
                messagebox.showinfo("Erfolg", f"Projekt gefunden: {response.data}")

                # Wechsle zum Input-Frame
                self.clear_frames()
                self.show_main_frame()
                
                # Rückgabe der Projektinformationen (optional, falls später benötigt)
                return self.project_number, self.project_short

            else:
                messagebox.showerror("Fehler", "Projekt nicht gefunden.")
                return None
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Projektsuche: {e}")
            return None


    def show_new_project_input(self):
        """
        Zeigt die Eingabemaske für ein neues Projekt.
        """
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
        
        self.add_logout_button_and_leave_project_button(self.project_input_frame)



    def create_project(self):
        """
        Erstellt ein neues Projekt und speichert es in der Datenbank.

        Rückgabe:
            tuple: (Projektnummer, Projektname, Projektkürzel, Anzahl Etappen), falls erfolgreich.
        """
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
            try:
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
        """
        Speichert ein neues Projekt in der Datenbank.

        Parameter:
            project_number (str): Projektnummer.
            project_name (str): Name des Projekts.
            project_short (str): Projektkürzel.
            project_stages (int): Anzahl der Etappen.
        """
        try:
            # Die Anfrage an die Supabase-Datenbank senden
            response = self.supabase.table("projekte").insert({
                "projektnummer": project_number,
                "projekt_name": project_name,
                "projekt_kuerzel": project_short,
                "anzahl_etappen": project_stages,
                "projekt_code" : f"{project_number}{project_short}".strip()
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
        """
        Überprüft, ob ein Projekt mit der angegebenen Nummer oder dem Kürzel bereits in der Datenbank existiert.

        Parameter:
            project_number (str): Projektnummer.
            project_short (str): Projektkürzel.

        Rückgabe:
            str: "both", wenn sowohl Nummer als auch Kürzel existieren,
                "short", wenn nur das Kürzel existiert,
                "none", wenn das Projekt nicht existiert.
        """
        try:
            # Erstelle den Projektcode aus Nummer und Kürzel
            project_code = f"{project_number}{project_short}"

            # Datenbankabfrage nach dem Projektcode
            response = self.supabase.table("projekte").select("projekt_code").filter("projekt_code", "eq", project_code).execute()

            if response.data:
                return "both"  # Der Projektcode existiert bereits

            # Falls nur das Kürzel existiert (andere Kombination)
            response_short = self.supabase.table("projekte").select("projekt_kuerzel").filter("projekt_kuerzel", "eq", project_short).execute()

            if response_short.data:
                return "short"  # Das Kürzel ist bereits vergeben, aber mit einer anderen Nummer

            return "none"  # Kein passendes Projekt gefunden

        except Exception as e:
            print(f"Fehler bei der Projektsuche: {e}")
            return "none"

    def open_existing_project(self):
        """
        Öffnet das Fenster zur Eingabe der Projektnummer, um ein bestehendes Projekt zu laden.
        """
        self.show_project_search_frame()

    def compare_projects(self):
        """
        Zeigt eine Benachrichtigung, dass die Vergleichsfunktion noch nicht verfügbar ist.
        """
        messagebox.showinfo(title="Hinweis", message="Coming Soon :)")


    def show_main_frame(self):
        """
        Zeigt das Hauptfenster nach erfolgreichem Login oder Projektauswahl.
        """
        # Neues Main Frame laden
        self.main_frame = create_main_frame(self.root)

        self.input_frame = create_input_frame(self.main_frame)
        self.result_frame = create_result_frame(self.main_frame)
        create_version_label(self.input_frame)  # Eingabebereich (linke Seite) - Unter dem Titelrahmen

        # Dateien Auswahl
        # Excel Armierung Alt
        self.xlsx_ausschreibung_label = ctk.CTkLabel(
        self.input_frame, 
        text="Armierung Ausschreibung", 
        font=("Helvetica", 14, "bold"), 
        fg_color="#787575", 
        text_color="#ffffff"
        )
        self.xlsx_ausschreibung_label.pack(pady=5, padx=10, fill="x")

        self.xlsx_ausschreibung_button = ctk.CTkButton(
            self.input_frame, 
            text="Excel Upload", 
            command=self.upload_reinforcement_auschreibung, 
            fg_color="#ffa8a8", 
            text_color="white", 
            width=200
        )
        self.xlsx_ausschreibung_button.pack(pady=(5, 5), padx=10)

        self.xlsx_ausschreibung_count_label = ctk.CTkLabel(
            self.input_frame, 
            text="Noch keine Datei hochgeladen", 
            font=("Helvetica", 12), 
            text_color="#ffffff"
        )
        self.xlsx_ausschreibung_count_label.pack(pady=(5, 10), padx=10, fill="x")

        # Eingabefeld für Datum der Unterzeichnung
        self.date_label = ctk.CTkLabel(
            self.input_frame, 
            text="Werkvertragsdatum", 
            font=("Helvetica", 14, "bold"), 
            fg_color="#787575", 
            text_color="#ffffff"
            )
        
        self.date_label.pack(pady=(10, 5), padx=10, fill="x")

        self.date_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="YYYY-MM-TT", 
            font=("Helvetica", 12), 
            width=200
        )
        self.date_entry.pack(pady=5, padx=10)

        # IFC Armierung Ausführung
        self.ifc_ausfuehrung_label = ctk.CTkLabel(
            self.input_frame, 
            text="Armierung Ausführung", 
            font=("Helvetica", 14, "bold"), 
            fg_color="#787575", 
            text_color="#ffffff"
        )
        self.ifc_ausfuehrung_label.pack(pady=(20, 5), padx=10, fill="x")

        self.ifc_ausfuehrung_button = ctk.CTkButton(
            self.input_frame, 
            text="IFC Upload", 
            command=self.upload_reinforcement_ausfuehrung, 
            fg_color="#ffa8a8", 
            text_color="white", 
            width=200
        )
        self.ifc_ausfuehrung_button.pack(pady=(5, 5), padx=10)

        self.ifc_ausfuehrung_count_label = ctk.CTkLabel(
            self.input_frame, 
            text="Noch keine Datei hochgeladen", 
            font=("Helvetica", 12), 
            text_color="#ffffff"
        )
        self.ifc_ausfuehrung_count_label.pack(pady=(5, 10), padx=10, fill="x")

        # Button zum Hochladen
        self.upload_button = ctk.CTkButton(
            self.input_frame, 
            text="Daten Uploaden", 
            font=("Helvetica", 14), 
            command=self.start_upload, 
            fg_color="#000000", 
            text_color="white", 
            width=200
        )
        self.upload_button.pack(pady=(20, 5), padx=10)

        # Status Label
        self.ausführungs_status_label = ctk.CTkLabel(
            self.input_frame, 
            text="Deine Daten wurden noch nicht \nauf die Datenbank hochgeladen", 
            font=("Helvetica", 12), 
            text_color="red"
        )
        self.ausführungs_status_label.pack(pady=(5, 10), padx=10, fill="x")

        # Button zum Analyse starten
        self.analyze_button = ctk.CTkButton(
            self.input_frame, 
            text="Analyse starten", 
            font=("Helvetica", 14), 
            command=self.start_analyze, 
            fg_color="#000000", 
            text_color="white", 
            width=200
        )
        self.analyze_button.pack(pady=(10, 20), padx=10)
        # Variablen zur Speicherung der Dateipfade
        self.ifc_old_paths = []
        self.ifc_new_paths = []

        self.add_logout_button_and_leave_project_button(self.input_frame)
    
    def clear_frames(self):
        """
        Entfernt alle aktiven Fenster, um Platz für neue Inhalte zu schaffen.
        """
        if hasattr(self, "login_frame") and self.login_frame:
            self.login_frame.pack_forget()
            self.login_frame.destroy()

        if hasattr(self, "selection_frame") and self.selection_frame:
            self.selection_frame.pack_forget()
            self.selection_frame.destroy()

        if hasattr(self, "main_frame") and self.main_frame:
            self.main_frame.pack_forget()
            self.main_frame.destroy()

        if hasattr(self, "project_input_frame") and self.project_input_frame:
            self.project_input_frame.pack_forget()
            self.project_input_frame.destroy()
        
        if hasattr(self, "project_search_frame") and self.project_search_frame:
            self.project_search_frame.pack_forget()
            self.project_search_frame.destroy()



    def toggle_fullscreen(self, event=None):
        """
        Aktiviert oder deaktiviert den Vollbildmodus.

        Parameter:
            event (tk.Event, optional): Tasteneingabe-Event.
        """
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        """
        Beendet den Vollbildmodus.

        Parameter:
            event (tk.Event, optional): Tasteneingabe-Event.
        """
        self.root.attributes("-fullscreen", False)

    def upload_reinforcement_auschreibung(self):
        """
        Öffnet einen Dialog zum Hochladen von Excel-Dateien für die Armierungsausschreibung.
        """
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel file", "*.xlsx")])
        if file_paths:
            self.xlsx_ausschreibung_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.xlsx_ausschreibung_button.configure(fg_color="#83fc83", text_color="white")
            self.xlsx_ausschreibung_count_label.configure(text=f"{len(file_paths)} Datei(en) hochgeladen")

    def upload_reinforcement_ausfuehrung(self):
        """
        Öffnet einen Dialog zum Hochladen von IFC-Dateien für die Armierungsausführung.
        """
        file_paths = filedialog.askopenfilenames(filetypes=[("IFC files", "*.ifc")])
        if file_paths:
            self.ifc_ausfuehrung_paths = list(file_paths)
            # Button grün markieren und den Status aktualisieren
            self.ifc_ausfuehrung_button.configure(fg_color="#83fc83", text_color="white")
            self.ifc_ausfuehrung_count_label.configure(text=f"{len(file_paths)} Datei(en) hochgeladen")

    def upload_excel_to_supabase(self, excel_file):
        """
        Lädt eine Excel-Tabelle mit Ausschreibungsdaten in die Datenbank hoch.

        Parameter:
            excel_file (str): Pfad zur Excel-Datei.
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
            project_code = f"{self.project_number}{self.project_short}"

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

    def start_upload(self):
        """
        Startet den Upload-Prozess für Ausschreibungs- und Ausführungsdaten.
        """
        try:
            # Prüfe, ob die Projektinformationen vorhanden sind
            if not hasattr(self, 'project_number') or not hasattr(self, 'project_short'):
                messagebox.showerror("Fehler", "Projektinformationen fehlen. Bitte erst ein Projekt erstellen.")
                return

            # IFC-Dateien analysieren, wenn vorhanden
            if hasattr(self, 'ifc_ausfuehrung_paths') and self.ifc_ausfuehrung_paths:
                analyze_reinforcement_data(self.ifc_ausfuehrung_paths, self.project_number, self.project_short)
                print("IFC-Dateien wurden erfolgreich analysiert.")
            else:
                print("Keine IFC-Dateien gefunden. Überspringe die Analyse.")

            # Excel-Dateien hochladen, wenn vorhanden
            if hasattr(self, "xlsx_ausschreibung_paths") and self.xlsx_ausschreibung_paths:
                # Prüfe, ob ein Datum eingegeben wurde
                creation_date = self.date_entry.get().strip()
                if not creation_date:
                    messagebox.showerror("Fehler", "Bitte geben Sie ein Datum an, bevor Sie Excel-Dateien hochladen.")
                    return

                # Schleife durch die Excel-Dateien
                for excel_file in self.xlsx_ausschreibung_paths:
                    print(f"Starte Upload für Datei: {excel_file}")
                    self.upload_excel_to_supabase(excel_file)

                print("Excel-Dateien wurden erfolgreich hochgeladen.")
            else:
                print("Keine Excel-Dateien gefunden. Überspringe den Upload.")

            # Status aktualisieren
            self.ausführungs_status_label.configure(text_color="green")
            self.ausführungs_status_label.configure(text=f"Deine Daten wurden erfolgreich \nauf die Datenbank hochgeladen")

            # Pfade und Eingaben zurücksetzen
            self.ifc_ausfuehrung_paths = []  # IFC-Dateien löschen
            self.xlsx_ausschreibung_paths = []  # Excel-Dateien löschen
            self.date_entry.delete(0, 'end')  # Datum löschen
            self.date_entry.configure(placeholder_text="YYYY-MM-DD")  # Platzhalter zurücksetzen
            self.ifc_ausfuehrung_count_label.configure(text="Noch keine Datei hochgeladen")  # IFC-Status zurücksetzen
            self.xlsx_ausschreibung_count_label.configure(text="Noch keine Datei hochgeladen")  # Excel-Status zurücksetzen
            self.ifc_ausfuehrung_button.configure(fg_color="#ffa8a8", text_color="white")  # IFC-Upload-Button zurücksetzen
            self.xlsx_ausschreibung_button.configure(fg_color="#ffa8a8", text_color="white")  # Excel-Upload-Button zurücksetzen

            messagebox.showinfo("Erfolg", "Analyse und Upload abgeschlossen.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Analyse oder beim Upload: {str(e)}")

    def fetch_and_display_data(self):
        """
        Holt Projektdaten aus der Datenbank und zeigt sie als scrollbare Tabellen an.
        """
        
        # Vorherige Inhalte des result_frame entfernen
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not hasattr(self, 'project_number') or not hasattr(self, 'project_short'):
            messagebox.showerror("Fehler", "Kein Projektcode gefunden. Bitte wähle zuerst ein Projekt aus.")
            return

        project_code = f"{self.project_number}{self.project_short}"

        # Daten aus der ersten Tabelle abrufen
        data_aggregated = []
        try:
            response = self.supabase.table("aggregated_reinforcement_data").select("*").filter("project_code_aggregated", "eq", project_code).execute()
            data_aggregated = response.data if response.data else []
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen der aggregierten Daten: {e}")
            return

        # Daten aus der zweiten Tabelle abrufen
        data_tender = []
        try:
            response = self.supabase.table("tender_data_reinforcement").select("*").filter("projekt_code", "eq", project_code).execute()
            data_tender = response.data if response.data else []
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen der Ausschreibungsdaten: {e}")
            return

        if not data_aggregated and not data_tender:
            messagebox.showinfo("Hinweis", f"Keine Daten für Projekt {project_code} gefunden.")
            return

        # Haupt-Frame für beide Tabellen
        table_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        # Obere Tabelle (Aggregated Reinforcement Data)
        if data_aggregated:
            self.create_scrollable_table(table_frame, data_aggregated, "Armierung Ausführung")

        # Untere Tabelle (Tender Data Reinforcement)
        if data_tender:
            self.create_scrollable_table(table_frame, data_tender, "Armierung Ausschreibung")

    def create_scrollable_table(self, parent, data, title):
        """
        Erstellt eine scrollbare Tabelle mit den angegebenen Daten.

        Parameter:
            parent (ctk.CTkFrame): Das übergeordnete UI-Element.
            data (list): Die anzuzeigenden Daten.
            title (str): Der Titel der Tabelle.
        """
        
        # Daten als Pandas DataFrame formatieren
        df = pd.DataFrame(data)

        # Frame für die Tabelle
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="both", expand=True, pady=10)

        # Titel über der Tabelle
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Helvetica", 16, "bold"))
        title_label.pack(pady=5)

        # Canvas für Scrollbarkeit
        canvas = ctk.CTkCanvas(section_frame)
        scrollbar_y = ctk.CTkScrollbar(section_frame, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Tabelle mit CustomTkinter erstellen
        tree = ttk.Treeview(scrollable_frame, columns=list(df.columns), show="headings", height=15)

        # Spaltenüberschriften setzen
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=200, anchor="center")  # Gleichmäßige Spaltenbreite

        # Zeilen in die Tabelle einfügen
        for row in df.itertuples(index=False):
            tree.insert("", "end", values=row)

        # Styling verbessern
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14), rowheight=30)

        tree.pack(fill="both", expand=True)

    def start_analyze(self):
        """
        Startet die Analyse der Armierungsdaten.
        """
        print("Analyse starten")
        self.fetch_and_display_data()