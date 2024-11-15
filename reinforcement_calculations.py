def calculate_reinforcement_summaries(reinforcement_data):
    """
    Berechnet die Zusammenfassungen der Armierungsdaten pro Etappe und Material.
    :param reinforcement_data: Liste der Armierungseigenschaften
    :return: Dictionary der Etappen mit den entsprechenden Materialsummen
    """
    # Dictionary für Etappen initialisieren
    etappen_data = {}

    # Über alle Armierungselemente iterieren
    for data in reinforcement_data:
        # Sicherstellen, dass `data` ein Dictionary ist
        if isinstance(data, dict):
            etappenbezeichnung = data.get("Etappenbezeichnung", "Unbekannte Etappe")
            stahlgruppen_gewicht = data.get("Stabgruppe Gewicht", 0.0)
            bauteilname = data.get("Bauteilname", "Unbekannt")

            # Etappe initialisieren, falls nicht vorhanden
            if etappenbezeichnung not in etappen_data:
                etappen_data[etappenbezeichnung] = {
                    "Gesamtgewicht": 0.0,
                    "Materialien": {}
                }

            # Gesamtgewicht für die Etappe aktualisieren
            etappen_data[etappenbezeichnung]["Gesamtgewicht"] += stahlgruppen_gewicht

            # Gewicht pro Material aktualisieren
            if bauteilname not in etappen_data[etappenbezeichnung]["Materialien"]:
                etappen_data[etappenbezeichnung]["Materialien"][bauteilname] = 0.0

            etappen_data[etappenbezeichnung]["Materialien"][bauteilname] += stahlgruppen_gewicht

    return etappen_data
