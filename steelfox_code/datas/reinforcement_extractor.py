def reinforcement_extract_properties(model):
    """
    Extrahiert und aggregiert die Eigenschaften der Armierung aus einem IFC-Modell.
    Die Daten werden aufgeteilt in Etappen > Material > Durchmesser und dann aggregiert.
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
                # Extrahierte Daten in eine flache Struktur umwandeln und zur Liste hinzufügen
                reinforcement_data.append({
                    "Etappenbezeichnung": etappenbezeichnung,
                    "Material": material,
                    "Durchmesser": durchmesser,
                    "Gesamtgewicht": stabgruppe_gewicht,
                    "AnzahlEisen": anzahl_eisen
                })

        return reinforcement_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return []