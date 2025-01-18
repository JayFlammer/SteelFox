import re

def extract_creation_date(filepath):
    """
    Extrahiert das Erstellungsdatum aus einer IFC-Datei.

    Parameter:
        filepath (str): Pfad zur IFC-Datei.

    Rückgabe:
        str: Erstellungsdatum im Format 'YYYY-MM-DD' oder 'Unbekannt'.
    """
    try:
        # Öffnet die Datei und liest sie Zeile für Zeile
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # Sucht nach der Zeile, die mit FILE_NAME beginnt
                if "FILE_NAME" in line:
                    # Regex, um das Datum im Format 'YYYY-MM-DDTHH:MM:SS' zu finden
                    match = re.search(r"\d{4}-\d{2}-\d{2}", line)
                    if match:
                        return match.group()  # Gibt das gefundene Datum zurück
        # Falls kein Datum gefunden wird
        return "Unbekannt"
    except Exception as e:
        print(f"Fehler beim Lesen der Datei für das Datum: {str(e)}")
        return "Unbekannt"

def extract_all_reinforcement_properties(model):
    """
    Extrahiert relevante Eigenschaften von IfcReinforcingBar-Elementen aus einem IFC-Modell.

    Parameter:
        model (ifcopenshell.file): Das IFC-Modell.

    Rückgabe:
        list: Eine Liste mit den extrahierten Eigenschaften.
    """
    try:
        # Headerinformationen extrahieren
        file_info = extract_creation_date(model)

        # Extrahiert alle IfcReinforcingBar-Elemente
        reinforcement_elements = model.by_type("IfcReinforcingBar")

        # Struktur für alle extrahierten Daten initialisieren
        reinforcement_data = []

        # Über alle Armierungselemente iterieren
        for element in reinforcement_elements:
            # Initialisiere Dictionary, um alle Informationen des Elements zu speichern
            element_data = {
                "GlobalId": element.GlobalId,
                "Name": element.Name,
                "Type": element.is_a(),
                "PropertySets": {},
                "Quantities": {},
                "Material": None,
                "FileInfo": file_info  # Füge die Meta-Informationen hinzu
            }

            # PropertySets des Elements durchsuchen
            if hasattr(element, 'IsDefinedBy'):
                for definition in element.IsDefinedBy:
                    if definition.is_a("IfcRelDefinesByProperties"):
                        property_set = definition.RelatingPropertyDefinition
                        if property_set.is_a("IfcPropertySet"):
                            pset_name = property_set.Name
                            element_data["PropertySets"][pset_name] = {}

                            # Alle Eigenschaften im PropertySet durchlaufen
                            for prop in property_set.HasProperties:
                                if prop.is_a("IfcPropertySingleValue"):
                                    property_name = prop.Name
                                    property_value = prop.NominalValue
                                    if property_value:
                                        element_data["PropertySets"][pset_name][property_name] = property_value.wrappedValue
                                    else:
                                        element_data["PropertySets"][pset_name][property_name] = "Kein Wert"

            # Materialinformationen extrahieren
            if hasattr(element, 'HasAssociations'):
                for association in element.HasAssociations:
                    if association.is_a("IfcRelAssociatesMaterial"):
                        material = association.RelatingMaterial
                        if hasattr(material, 'Name'):
                            element_data["Material"] = material.Name

            # Mengeninformationen extrahieren (falls verfügbar)
            if hasattr(element, 'IsDefinedBy'):
                for definition in element.IsDefinedBy:
                    if definition.is_a("IfcRelDefinesByProperties") and hasattr(definition, 'RelatingPropertyDefinition'):
                        if definition.RelatingPropertyDefinition.is_a("IfcElementQuantity"):
                            quantity_set = definition.RelatingPropertyDefinition
                            for quantity in quantity_set.Quantities:
                                element_data["Quantities"][quantity.Name] = quantity.NominalValue.wrappedValue if hasattr(quantity, 'NominalValue') else "Kein Wert"

            # Alle Eigenschaften des Elements in die Liste der Armierungsdaten einfügen
            reinforcement_data.append(element_data)

        return reinforcement_data

    except Exception as e:
        print(f"Fehler beim Extrahieren der Armierungseigenschaften: {str(e)}")
        return []
