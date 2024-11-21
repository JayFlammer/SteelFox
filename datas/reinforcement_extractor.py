import ifcopenshell
from ifcopenshell.util import element, pset

def reinforcement_extract_properties(model):
    """
    Extrahiert und aggregiert die Eigenschaften der Armierung aus einem IFC-Modell.
    Die Daten werden aufgeteilt in Etappen (Listennummer) > Material > Durchmesser und dann aggregiert.
    :param model: IFC Modell
    :return: Aggregierte Armierungseigenschaften als Liste von Dictionaries
    """
    try:
        # Extrahiert alle IfcReinforcingBar-Elemente
        reinforcement_elements = model.by_type("IfcReinforcingBar")

        # Struktur für aggregierte Daten initialisieren: Etappe > Material > Durchmesser
        reinforcement_data = []

        # Über alle Armierungselemente iterieren
        for element in reinforcement_elements:
            # Initialisiere die Variablen
            listennummer = None  # Entspricht der Etappenbezeichnung
            material = None
            durchmesser = None
            stabgruppe_gewicht = 0.0

            # PropertySets des Elements durchsuchen
            psets = pset.get_psets(element)

            # HGL_B2F PropertySet überprüfen und benötigte Eigenschaften extrahieren
            if "HGL_B2F" in psets:
                listennummer = psets["HGL_B2F"].get("Etappenbezeichnung")
                durchmesser = psets["HGL_B2F"].get("Durchmesser")
                stabgruppe_gewicht = psets["HGL_B2F"].get("Stabgruppe Gewicht", 0.0)

                # Um sicherzustellen, dass wir die Werte korrekt verarbeiten
                listennummer = listennummer.wrappedValue if listennummer else None
                durchmesser = durchmesser.wrappedValue if durchmesser else None
                stabgruppe_gewicht = stabgruppe_gewicht.wrappedValue if stabgruppe_gewicht else 0.0

            # Materialinformationen extrahieren
            material = element.get_material(element)

            # Nur weiter machen, wenn wir alle nötigen Informationen haben
            if listennummer and material and durchmesser:
                # Extrahierte Daten in eine flache Struktur umwandeln und zur Liste hinzufügen
                reinforcement_data.append({
                    "Listennummer": listennummer,
                    "Material": material.Name if material else "Unbekannt",
                    "Durchmesser": durchmesser,
                    "Gesamtgewicht": stabgruppe_gewicht
                })

        return reinforcement_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return []

