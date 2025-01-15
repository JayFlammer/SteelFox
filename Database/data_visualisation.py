import os
from supabase import create_client
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

# Laden der Umgebungsvariablen
load_dotenv()

# Supabase-Zugangsdaten abrufen
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

# Supabase-Client erstellen
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)
else:
    raise Exception("SUPABASE_URL und SUPABASE_API_KEY sind erforderlich.")

def fetch_aggregated_data():
    try:
        # Debugging: Zeige den Rückgabewert
        response = supabase.rpc("aggregated_reinforcement_data", {})
        print(f"Rückgabewert von RPC: {response}")
        return response
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []




# Daten in einer Tabelle mit Matplotlib darstellen
def display_data_as_table(data):
    if not data:
        print("Keine Daten vorhanden, um sie anzuzeigen.")
        return

    # Umwandeln der Daten in einen Pandas DataFrame
    df = pd.DataFrame(data)

    # Plotten der Tabelle
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.show()

# Daten abrufen und anzeigen
if __name__ == "__main__":
    data = fetch_aggregated_data()
    display_data_as_table(data)
