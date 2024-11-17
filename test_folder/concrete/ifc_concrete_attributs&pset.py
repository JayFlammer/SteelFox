import ifcopenshell

# Pfad zur IFC-Datei (Bitte Pfad anpassen)
ifc_file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Schalung\MC1_TRW_GRO_104-SCH_A_Schalung Boden und Wände 4.OG, Haus C1.ifc"

# IFC-Modell laden
model = ifcopenshell.open(ifc_file_path)

# Liste der Elementtypen, die wir untersuchen möchten
element_types = ["IfcWall", "IfcSlab"]

# Durchsuche die IFC-Datei nach den gesuchten Elementtypen
for element_type in element_types:
    elements = model.by_type(element_type)
    
    if elements:
        element = elements[0]  # Nur ein Beispiel-Element je Typ ausgeben
        print(f"\nElement ID: {element.GlobalId}, Typ: {element.is_a()}\n")

        # 1. Standard Attribute
        print("-- Standard Attribute --")
        attributes = element.get_info()  # Gibt ein Dictionary mit allen Attributen zurück
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

        # 2. PropertySets und deren Eigenschaften
        print("\n-- PropertySets und deren Eigenschaften --")
        if hasattr(element, 'IsDefinedBy'):
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a("IfcPropertySet"):
                        print(f"\n  PropertySet Name: {property_set.Name}")
                        for prop in property_set.HasProperties:
                            # Je nach Property-Typ unterschiedlich behandeln
                            if prop.is_a("IfcPropertySingleValue"):
                                property_name = prop.Name
                                property_value = prop.NominalValue
                                if property_value:
                                    print(f"    {property_name}: {property_value.wrappedValue}")
                                else:
                                    print(f"    {property_name}: Kein Wert")
                            elif prop.is_a("IfcPropertyEnumeratedValue"):
                                property_name = prop.Name
                                values = [val.wrappedValue for val in prop.EnumerationValues]
                                print(f"    {property_name}: {values}")
                            elif prop.is_a("IfcPropertyListValue"):
                                property_name = prop.Name
                                values = [val.wrappedValue for val in prop.ListValues]
                                print(f"    {property_name}: {values}")
                            elif prop.is_a("IfcPropertyTableValue"):
                                property_name = prop.Name
                                values = {
                                    'Defining Values': [val.wrappedValue for val in prop.DefiningValues],
                                    'Defined Values': [val.wrappedValue for val in prop.DefinedValues]
                                }
                                print(f"    {property_name}: {values}")

        # 3. Materialinformationen
        print("\n-- Materialinformationen --")
        if hasattr(element, 'HasAssociations'):
            for association in element.HasAssociations:
                if association.is_a("IfcRelAssociatesMaterial"):
                    material = association.RelatingMaterial
                    if material.is_a("IfcMaterial"):
                        print(f"Material: {material.Name}")
                    elif material.is_a("IfcMaterialLayerSetUsage") or material.is_a("IfcMaterialLayer"):
                        if hasattr(material, 'ForLayerSet'):
                            for layer in material.ForLayerSet.MaterialLayers:
                                print(f"Materialschicht: {layer.Material.Name}")

        # 4. Mengen (Quantities)
        print("\n-- Mengeninformationen --")
        if hasattr(element, 'IsDefinedBy'):
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    if hasattr(definition, 'RelatingPropertyDefinition'):
                        property_definition = definition.RelatingPropertyDefinition
                        if property_definition.is_a("IfcElementQuantity"):
                            print(f"\n  Mengen Name: {property_definition.Name}")
                            # Alle Quantities des Mengenordners durchlaufen
                            for quantity in property_definition.Quantities:
                                quantity_name = quantity.Name
                                
                                if quantity.is_a("IfcQuantityLength"):
                                    quantity_value = quantity.LengthValue
                                    print(f"    {quantity_name}: {quantity_value} m")
                                elif quantity.is_a("IfcQuantityArea"):
                                    quantity_value = quantity.AreaValue
                                    print(f"    {quantity_name}: {quantity_value} m²")
                                elif quantity.is_a("IfcQuantityVolume"):
                                    quantity_value = quantity.VolumeValue
                                    print(f"    {quantity_name}: {quantity_value} m³")

        # 5. Geometrie-Informationen
        print("\n-- Geometrie-Informationen --")
        if hasattr(element, 'Representation') and element.Representation:
            representation = element.Representation
            for rep in representation.Representations:
                print(f"Representation Name: {rep.Name if hasattr(rep, 'Name') else 'Nicht verfügbar'}")
                print(f"Representation Type: {rep.RepresentationType if hasattr(rep, 'RepresentationType') else 'Nicht verfügbar'}")

        # 6. Beziehungen des Elements
        print("\n-- Beziehungen des Elements --")
        relationships = [
            'HasOpenings', 'HasCoverings', 'IsDefinedBy', 'HasAssociations',
            'IsTypedBy', 'HasStructuralMember', 'ContainedInStructure'
        ]
        for relation in relationships:
            if hasattr(element, relation):
                related_items = getattr(element, relation)
                if related_items:
                    print(f"\nBeziehungstyp: {relation}")
                    for item in related_items:
                        print(f"  - {item.is_a()} (ID: {item.GlobalId if hasattr(item, 'GlobalId') else 'N/A'})")

        # Breche die Schleife nach dem ersten Element dieses Typs ab, um eine übersichtliche Ausgabe zu gewährleisten
        break

print("\n-- Ende der Übersicht --")
