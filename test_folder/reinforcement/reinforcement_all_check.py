import ifcopenshell

# Pfad zur IFC-Datei (Bitte Pfad anpassen)
ifc_file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Bewehrung\Decke\MET_TRW_GRO_098-BEW-BP-ET01_B_Bewehrung Vertiefungen ET1.ifc"

# IFC-Modell laden
model = ifcopenshell.open(ifc_file_path)

# Liste der Armierungselementtypen, die wir untersuchen
reinforcement_types = ["IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor"]

# Nur das erste gefundene Element anzeigen, um die Übersicht einfach zu halten
for reinforcement_type in reinforcement_types:
    reinforcements = model.by_type(reinforcement_type)
    
    if reinforcements:
        reinforcement = reinforcements[0]
        print(f"\nElement ID: {reinforcement.GlobalId}, Typ: {reinforcement.is_a()}\n")

        # 1. Standard Attribute
        print("-- Standard Attribute --")
        attributes = reinforcement.get_info()  # Gibt ein Dictionary mit allen Attributen zurück
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

        # 2. PropertySets und deren Eigenschaften
        print("\n-- PropertySets und deren Eigenschaften --")
        if hasattr(reinforcement, 'IsDefinedBy'):
            for definition in reinforcement.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a("IfcPropertySet"):
                        print(f"\n  PropertySet Name: {property_set.Name}")
                        for prop in property_set.HasProperties:
                            if prop.is_a("IfcPropertySingleValue"):
                                property_name = prop.Name
                                property_value = prop.NominalValue
                                if property_value:
                                    print(f"    {property_name}: {property_value.wrappedValue}")
                                else:
                                    print(f"    {property_name}: Kein Wert")

        # 3. Materialinformationen
        print("\n-- Materialinformationen --")
        if hasattr(reinforcement, 'HasAssociations'):
            for association in reinforcement.HasAssociations:
                if association.is_a("IfcRelAssociatesMaterial"):
                    material = association.RelatingMaterial
                    if material.is_a("IfcMaterial"):
                        print(f"Material: {material.Name}")
                    elif material.is_a("IfcMaterialLayerSetUsage") or material.is_a("IfcMaterialLayer"):
                        if hasattr(material, 'ForLayerSet'):
                            for layer in material.ForLayerSet.MaterialLayers:
                                print(f"Materialschicht: {layer.Material.Name}")

        # 4. Geometrie-Informationen
        print("\n-- Geometrie-Informationen --")
        if hasattr(reinforcement, 'Representation') and reinforcement.Representation:
            representation = reinforcement.Representation
            for rep in representation.Representations:
                print(f"Representation Name: {rep.Name if hasattr(rep, 'Name') else 'Nicht verfügbar'}")
                print(f"Representation Type: {rep.RepresentationType if hasattr(rep, 'RepresentationType') else 'Nicht verfügbar'}")

        # 5. Beziehungen des Elements
        print("\n-- Beziehungen des Elements --")
        relationships = [
            'HasOpenings', 'HasCoverings', 'IsDefinedBy', 'HasAssociations', 
            'IsTypedBy', 'HasStructuralMember'
        ]
        for relation in relationships:
            if hasattr(reinforcement, relation):
                related_items = getattr(reinforcement, relation)
                if related_items:
                    print(f"\nBeziehungstyp: {relation}")
                    for item in related_items:
                        print(f"  - {item.is_a()} (ID: {item.GlobalId if hasattr(item, 'GlobalId') else 'N/A'})")

        break  # Breche die Schleife nach dem ersten Element ab, um eine übersichtliche Ausgabe zu gewährleisten

print("\n-- Ende der Übersicht --")
