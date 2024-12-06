import pandas as pd

# Datei und Blattname angeben
excel_datei = r"C:\Users\FLJ\OneDrive - Halter AG\Armierung_Ausschreibung.xlsx"  # Pfad zur Excel-Datei
blatt_name = "Ausschreibung"     # Tabellenname im Excel

# Excel-Datei auslesen
try:
    df = pd.read_excel(excel_datei, sheet_name=blatt_name, engine="openpyxl")
    # Nur relevante Spalten auswählen (optional)
    df = df[['NPK', 'Menge', 'Preis']]

    # Daten anzeigen
    print(df)
except FileNotFoundError:
    print(f"Die Datei {excel_datei} wurde nicht gefunden.")
except ValueError:
    print(f"Das Blatt '{blatt_name}' existiert nicht in der Datei.")
