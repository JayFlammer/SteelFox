import ifcopenshell

def load_ifc_data(file_path):
    """
    Lädt eine IFC-Datei und gibt das Modell zurück.
    :param file_path: Pfad zur IFC-Datei
    :return: IFC Modell
    """
    return ifcopenshell.open(file_path)

import ifcopenshell

def concrete_extract_wall_slab_properties(model):
    try:
                # Elemente durchsuchen (IfcWall und IfcSlab)
        elements = model.by_type("IfcWall") + model.by_type("IfcSlab")

        # Ergebnisliste initialisieren
        result = []

        # Über alle Elemente iterieren
        for element in elements:
            # PropertySets des Elements durchsuchen
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition
                    # Prüfen, ob es ein PropertySet ist und ob der Name "HGL_GEO" lautet
                    if property_set.is_a("IfcPropertySet") and property_set.Name == "HGL_GEO":
                        # Properties durchsuchen und nach "Dicke" und "Flaeche" suchen
                        dicke = None
                        flaeche = None
                        for prop in property_set.HasProperties:
                            if prop.Name == "Dicke":
                                dicke = prop.NominalValue.wrappedValue
                            elif prop.Name == "Flaeche":
                                flaeche = prop.NominalValue.wrappedValue
                        
                        # Wenn beide Werte gefunden wurden, Ergebnis speichern
                        if dicke is not None and flaeche is not None:
                            result.append({
                                "ElementID": element.GlobalId,
                                "ElementTyp": element.is_a(),
                                "Dicke": dicke,
                                "Flaeche": flaeche
                            })

        # Ergebnisse ausgeben
        for res in result:
            print(f"Element ID: {res['ElementID']}, Typ: {res['ElementTyp']}, Dicke: {res['Dicke']} m, Flaeche: {res['Flaeche']} m²")

    except Exception as e:
        print(f"Fehler beim Lesen der IFC-Datei: {str(e)}")



def reinforcement_extract_properties(model):
    """
    Extrahiert die Eigenschaften der Armierung aus einem IFC-Modell basierend auf dem PropertySet "HGL_B2F".
    :param model: IFC Modell
    :return: Liste der Armierungseigenschaften
    """
    try:
        # Extrahiert alle IfcReinforcingBar-Elemente
        reinforcement_elements = model.by_type("IfcReinforcingBar")

        # Ergebnisliste initialisieren
        reinforcement_data = []

        # Über alle Armierungselemente iterieren
        for element in reinforcement_elements:
            # PropertySets des Elements durchsuchen
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition

                    # Prüfen, ob es ein PropertySet ist und ob der Name "HGL_B2F" lautet
                    if property_set.is_a("IfcPropertySet") and property_set.Name == "HGL_B2F":
                        armierung_props = {
                            "ElementID": element.GlobalId,
                            "ElementTyp": element.is_a()
                        }

                        for prop in property_set.HasProperties:
                            if prop.Name in [
                                "Bauteilname", "Listennummer", "Etappenbezeichnung",
                                "Bewehrungslage", "Positionsnummer", "Anzahl Eisen",
                                "Durchmesser", "Teilung", "Eisenlänge",
                                "Bewehrungsbeschriftung", "Stabgewicht",
                                "Stabgruppe Gewicht", "Betonierabschnitt"
                            ]:
                                armierung_props[prop.Name] = prop.NominalValue.wrappedValue

                        # Extrahierte Eigenschaften zur Ergebnisliste hinzufügen
                        reinforcement_data.append(armierung_props)

        return reinforcement_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return []