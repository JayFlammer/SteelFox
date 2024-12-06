import pandas as pd
from supabase import create_client, Client

# Supabase-Zugangsdaten
supabase_url = "https://your-supabase-url.supabase.co"  # Ersetze durch deine URL
supabase_key = "your-supabase-api-key"  # Ersetze durch deinen API-Schlüssel
supabase: Client = create_client(supabase_url, supabase_key)

# Datei- und Blattnamen
excel_datei = "deine_datei.xlsx"  # Ersetze mit dem Pfad zu deiner Datei
blatt_name = "Ausschreibung"     # Tabellenname im Excel

# Excel-Daten lesen
try:
    df = pd.read_excel(excel_datei, sheet_name=blatt_name, engine="openpyxl")
    # Nur relevante Spalten auswählen
    df = df[['NPK', 'Menge', 'Preis']]
    
    # Pakete erstellen
    pakete = {}
    for _, row in df.iterrows():
        npk = row["NPK"]
        pakete[npk] = {"Menge": row["Menge"], "Preis": row["Preis"]}
    
    # Daten auf Supabase hochladen
    for npk, details in pakete.items():
        response = supabase.table("ausschreibung").insert({
            "NPK": npk,
            "Menge": details["Menge"],
            "Preis": details["Preis"]
        }).execute()
        print(f"NPK {npk} hochgeladen: {response.status_code} - {response.data}")

except FileNotFoundError:
    print(f"Die Datei {excel_datei} wurde nicht gefunden.")
except ValueError:
    print(f"Das Blatt '{blatt_name}' existiert nicht in der Datei.")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")

