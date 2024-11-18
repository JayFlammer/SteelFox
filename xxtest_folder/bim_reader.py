import ifcopenshell
def read_bim_data(element):
    """
    Liest die BIM-Daten eines Elements und gibt sie zurück.
    :param element: IFC Element
    :return: Dictionary mit BIM-Daten
    """
    bim_data = {
        "GlobalId": element.GlobalId,
        "Typ": element.is_a(),
        "Name": getattr(element, "Name", "Nicht definiert"),
        "Beschreibung": getattr(element, "Description", "Nicht definiert"),
    }

    # Alle PropertySets des Elements durchlaufen
    for definition in element.IsDefinedBy:
        if definition.is_a("IfcRelDefinesByProperties"):
            property_set = definition.RelatingPropertyDefinition
            if property_set.is_a("IfcPropertySet"):
                properties = {}
                for prop in property_set.HasProperties:
                    properties[prop.Name] = prop.NominalValue.wrappedValue if hasattr(prop, "NominalValue") else str(prop.NominalValue)
                
                bim_data[property_set.Name] = properties

    return bim_data

# Beispiel zur Verwendung
if __name__ == "__main__":
    file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Bewehrung\Decke\MET_TRW_GRO_098-BEW-BP-ET01_B_Bewehrung Vertiefungen ET1.ifc"
    model = ifcopenshell.open(file_path)

    # Nimm als Beispiel das erste Element des Typs IfcWall
    walls = model.by_type("IfcWall")
    if walls:
        wall = walls[0]
        wall_data = read_bim_data(wall)

        # Zeige alle BIM-Daten des Elements an
        for key, value in wall_data.items():
            if isinstance(value, dict):
                print(f"PropertySet: {key}")
                for prop_key, prop_value in value.items():
                    print(f"  {prop_key}: {prop_value}")
            else:
                print(f"{key}: {value}")