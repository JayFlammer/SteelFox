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

# Daten aus Supabase View abrufen für einen bestimmten Projektcode
def fetch_data_for_project_code(project_code):
    try:
        # Abruf der Daten mit Filterung nach project_code_aggregated
        response = supabase.table("aggregated_reinforcement_data").select("*").eq("project_code_aggregated", project_code).execute()
        if response.data:
            print(f"Daten erfolgreich abgerufen für Projektcode {project_code}.")
            return response.data
        else:
            print(f"Keine Daten für den Projektcode {project_code} gefunden.")
            return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []

# Daten in einer Tabelle mit Matplotlib darstellen
def display_data_as_table(data, project_code):
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
    plt.title(f"Daten für Projektcode: {project_code}")
    plt.show()

# Eingabefunktion für den Projektcode
def get_project_code_from_user():
    project_code = input("Bitte gib den Projektcode ein (z. B. 5572EMW): ")
    return project_code.strip()

# Daten abrufen und anzeigen
if __name__ == "__main__":
    project_code = get_project_code_from_user()
    data = fetch_data_for_project_code(project_code)
    display_data_as_table(data, project_code)
