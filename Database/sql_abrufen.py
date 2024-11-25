import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Laden der Umgebungsvariablen
load_dotenv()  # Lädt die Variablen aus der .env Datei

# Supabase-Zugangsdaten abrufen
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

# Supabase-Client erstellen
if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    raise Exception("SUPABASE_URL und SUPABASE_API_KEY sind erforderlich.")

# Funktion zum Abrufen der Preise
def get_prices():
    try:
        response = supabase.table("preise").select("preisindex").execute()
        # Prüfen, ob Daten in der Antwort enthalten sind
        if response.data:
            # Daten abrufen und ausgeben
            preise = response.data
            for preis in preise:
                print(preis)
        else:
            print("Keine Daten gefunden oder ein Fehler ist aufgetreten.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Preise abrufen
get_prices()
