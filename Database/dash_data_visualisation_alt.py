import os
from supabase import create_client
import pandas as pd
from dotenv import load_dotenv
from dash import Dash, dash_table

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

# Daten aus Supabase View abrufen
def fetch_aggregated_data():
    try:
        response = supabase.table("aggregated_reinforcement_data").select("*").execute()
        if response.data:
            print("Daten erfolgreich abgerufen.")
            return response.data
        else:
            print("Keine Daten gefunden.")
            return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []

# Dash-App erstellen
def create_dash_table(data):
    if not data:
        print("Keine Daten vorhanden, um sie anzuzeigen.")
        return

    # Umwandeln der Daten in einen Pandas DataFrame
    df = pd.DataFrame(data)

    # Dash-App erstellen
    app = Dash(__name__)
    app.layout = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={"height": "600px", "overflowY": "auto"},
        style_cell={"textAlign": "left", "minWidth": "120px", "width": "120px", "maxWidth": "200px"},
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        page_size=20,
    )

    return app

# Daten abrufen und Dash starten
if __name__ == "__main__":
    data = fetch_aggregated_data()
    dash_app = create_dash_table(data)
    if dash_app:
        dash_app.run_server(debug=True, use_reloader=False)
