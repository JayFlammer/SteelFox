def extract_file_info(model):
    """
    Extrahiert allgemeine Metainformationen aus dem IFC-Modell.
    :param model: IFC Modell
    :return: Dictionary mit allgemeinen Metainformationen
    """
    try:
        header = model.header
        file_info = {
            "CreationTime": header.file_creation_date if hasattr(header, 'file_creation_date') else "Unbekannt",
            "Author": header.file_author if hasattr(header, 'file_author') else "Unbekannt",
            "Organization": header.file_organization if hasattr(header, 'file_organization') else "Unbekannt",
            "Filename": header.file_name if hasattr(header, 'file_name') else "Unbekannt"
        }
        return file_info
    except Exception as e:
        print(f"Fehler beim Extrahieren der Datei-Informationen: {str(e)}")
        return {
            "CreationTime": "Unbekannt",
            "Author": "Unbekannt",
            "Organization": "Unbekannt",
            "Filename": "Unbekannt"
        }

def extract_all_reinforcement_properties(model):
    """
    Extrahiert alle Eigenschaften, PropertySets und Materialinformationen aus einem IFC-Modell.
    Die Funktion gibt eine umfassende Liste von Eigenschaften jeder IfcReinforcingBar zurück,
    einschließlich der allgemeinen Metainformationen des Modells.
    
    :param model: IFC Modell
    :return: Liste von Dictionaries, die alle relevanten Eigenschaften enthalten
    """
    try:
        # Headerinformationen extrahieren
        file_info = extract_file_info(model)

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
