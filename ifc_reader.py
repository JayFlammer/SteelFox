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

def old_extract_wall_and_slab_data(model):
    """
    Extrahiert die Dicke und Fläche der Wände und Decken.
    :param model: IFC Modell
    :return: Liste der Elemente mit Dicke und Fläche
    """
    elements = model.by_type('IfcWall') + model.by_type('IfcSlab')
    data = []
    for element in elements:
        try:
            hgl_geo = element.IsDefinedBy[0].RelatingPropertyDefinition
            dicke = getattr(hgl_geo, 'Thickness', 0)
            flaeche = getattr(hgl_geo, 'Area', 0)
            data.append((dicke, flaeche))
        except AttributeError:
            continue  # Überspringe das Element, wenn die Eigenschaften fehlen
    return data

def reinforcement_extract_properties(model):
    """
    Extrahiert die Eigenschaften der Armierung aus einem IFC-Modell basierend auf dem PropertySet "HGL_B2F" und gruppiert die Daten pro Etappe.
    :param model: IFC Modell
    :return: Dictionary der Etappen mit den entsprechenden Materialsummen
    """
    try:
        # Extrahiert alle IfcReinforcingBar-Elemente
        reinforcement_elements = model.by_type("IfcReinforcingBar")

        # Dictionary für Etappen initialisieren
        etappen_data = {}

        # Über alle Armierungselemente iterieren
        for element in reinforcement_elements:
            # PropertySets des Elements durchsuchen
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition

                    # Prüfen, ob es ein PropertySet ist und ob der Name "HGL_B2F" lautet
                    if property_set.is_a("IfcPropertySet") and property_set.Name == "HGL_B2F":
                        etappenbezeichnung = None
                        stahlgruppen_gewicht = None

                        # Properties extrahieren
                        for prop in property_set.HasProperties:
                            if prop.Name == "Etappenbezeichnung":
                                etappenbezeichnung = prop.NominalValue.wrappedValue
                            elif prop.Name == "Stabgruppe Gewicht":
                                stahlgruppen_gewicht = prop.NominalValue.wrappedValue

                        # Wenn die Etappenbezeichnung und das Gewicht vorhanden sind, hinzufügen
                        if etappenbezeichnung and stahlgruppen_gewicht is not None:
                            if etappenbezeichnung not in etappen_data:
                                etappen_data[etappenbezeichnung] = {
                                    "Gesamtgewicht": 0.0,
                                    "Materialien": {}
                                }
                            etappen_data[etappenbezeichnung]["Gesamtgewicht"] += stahlgruppen_gewicht

                            # Bauteilname hinzufügen, um die Materialien zusammenzufassen
                            bauteilname = None
                            for prop in property_set.HasProperties:
                                if prop.Name == "Bauteilname":
                                    bauteilname = prop.NominalValue.wrappedValue

                            if bauteilname:
                                if bauteilname not in etappen_data[etappenbezeichnung]["Materialien"]:
                                    etappen_data[etappenbezeichnung]["Materialien"][bauteilname] = 0.0
                                etappen_data[etappenbezeichnung]["Materialien"][bauteilname] += stahlgruppen_gewicht

        return etappen_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return {}

