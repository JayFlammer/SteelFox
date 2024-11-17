import ifcopenshell
from collections import defaultdict

def reinforcement_extract_properties(model):
    """
    Extrahiert und aggregiert die Eigenschaften der Armierung aus einem IFC-Modell.
    Die Daten werden aufgeteilt in Etappen > Material > Durchmesser und dann aggregiert.
    :param model: IFC Modell
    :return: Aggregierte Armierungseigenschaften
    """
    try:
        # Extrahiert alle IfcReinforcingBar-Elemente
        reinforcement_elements = model.by_type("IfcReinforcingBar")

        # Struktur für aggregierte Daten initialisieren: Etappe > Material > Durchmesser
        reinforcement_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"Gesamtgewicht": 0.0, "AnzahlEisen": 0})))

        # Über alle Armierungselemente iterieren
        for element in reinforcement_elements:
            etappenbezeichnung = None
            material = None
            durchmesser = None
            anzahl_eisen = 0
            stabgruppe_gewicht = 0.0

            # PropertySets des Elements durchsuchen
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition

                    # Prüfen, ob es ein PropertySet ist und ob der Name "HGL_B2F" lautet
                    if property_set.is_a("IfcPropertySet") and property_set.Name == "HGL_B2F":
                        for prop in property_set.HasProperties:
                            if prop.Name == "Etappenbezeichnung":
                                etappenbezeichnung = prop.NominalValue.wrappedValue
                            elif prop.Name == "Durchmesser":
                                durchmesser = prop.NominalValue.wrappedValue
                            elif prop.Name == "Anzahl Eisen":
                                anzahl_eisen = prop.NominalValue.wrappedValue
                            elif prop.Name == "Stabgruppe Gewicht":
                                stabgruppe_gewicht = prop.NominalValue.wrappedValue

            # Materialinformationen extrahieren
            if hasattr(element, 'HasAssociations'):
                for association in element.HasAssociations:
                    if association.is_a("IfcRelAssociatesMaterial"):
                        material_def = association.RelatingMaterial
                        if material_def.is_a("IfcMaterial"):
                            material = material_def.Name

            # Nur weiter machen, wenn wir alle nötigen Informationen haben
            if etappenbezeichnung and material and durchmesser:
                # Daten zur aggregierten Struktur hinzufügen
                reinforcement_data[etappenbezeichnung][material][durchmesser]["Gesamtgewicht"] += stabgruppe_gewicht
                reinforcement_data[etappenbezeichnung][material][durchmesser]["AnzahlEisen"] += anzahl_eisen

        # Ausgabe der aggregierten Daten
        for etappe, materials in reinforcement_data.items():
            print(f"\nEtappe: {etappe}")
            for mat, diameters in materials.items():
                print(f"  Material: {mat}")
                for dia, data in diameters.items():
                    print(f"    Durchmesser: {dia}")
                    print(f"      Gesamtgewicht: {data['Gesamtgewicht']} kg")
                    print(f"      Anzahl Eisen: {data['AnzahlEisen']}")

        return reinforcement_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return {}

# Beispielaufruf (Pfad zur IFC-Datei anpassen)
ifc_file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Bewehrung\Decke\MET_TRW_GRO_098-BEW-BP-ET01_B_Bewehrung Vertiefungen ET1.ifc"
model = ifcopenshell.open(ifc_file_path)
reinforcement_extract_properties(model)
