import ifcopenshell

# Datei laden
model = ifcopenshell.open(r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Schalung\MC1_TRW_GRO_104-SCH_A_Schalung Boden und Wände 4.OG, Haus C1.ifc")


# Erste Wand im Modell auswählen
wall = model.by_type("IfcWall")[0]

# Alle Attribute der Wand auslesen
print(f"Element ID: {wall.GlobalId}, Typ: {wall.is_a()}")

# Ausgabe aller Standardattribute des Elements (IfcWall)
print("\n-- Standard Attribute --")
attributes = wall.get_info()  # Diese Methode liefert ein Dictionary mit allen Attributen
for attr_name, attr_value in attributes.items():
    print(f"{attr_name}: {attr_value}")

# Alle Beziehungen (z.B. zu PropertySets) auslesen
print("\n-- Beziehungen und PropertySets --")
for definition in wall.IsDefinedBy:
    if definition.is_a("IfcRelDefinesByProperties"):
        property_set = definition.RelatingPropertyDefinition

        # Prüfen, ob das PropertySet ein IfcPropertySet ist
        if property_set.is_a("IfcPropertySet"):
            print(f"\n  PropertySet Name: {property_set.Name}")

            # Alle Eigenschaften im PropertySet durchlaufen
            for prop in property_set.HasProperties:
                if prop.is_a("IfcPropertySingleValue"):
                    property_name = prop.Name
                    property_value = prop.NominalValue

                    # Wert überprüfen und korrekt ausgeben
                    if property_value:
                        print(f"    {property_name}: {property_value.wrappedValue}")
                    else:
                        print(f"    {property_name}: Kein Wert")

# Geometrieinformationen und andere komplexe Attribute ausgeben
print("\n-- Geometrie- und weitere Details --")

# Falls das Wand-Element Geometrie enthält, wird diese hier ausgegeben
if wall.Representation:
    representation = wall.Representation

    # Einige IFC-Objekte haben möglicherweise kein 'RepresentationIdentifier', daher zuerst prüfen
    if hasattr(representation, "RepresentationIdentifier"):
        print(f"Representation Identifier: {representation.RepresentationIdentifier}")
    else:
        print("Representation Identifier: Nicht verfügbar")

    # Typ der Repräsentation
    if hasattr(representation, "RepresentationType"):
        print(f"Representation Type: {representation.RepresentationType}")
    else:
        print("Representation Type: Nicht verfügbar")

    # Alle geometrischen Darstellungen (z.B. IfcShapeRepresentation) durchlaufen
    for rep in representation.Representations:
        print(f"  Representation Name: {rep.Name if hasattr(rep, 'Name') else 'Nicht verfügbar'}")
        print(f"  Representation Type: {rep.RepresentationType if hasattr(rep, 'RepresentationType') else 'Nicht verfügbar'}")

# Beziehungen, z.B. zur Zuweisung an ein Projekt oder Standort
print("\n-- Zugehörige Beziehungen --")
if hasattr(wall, "IsContainedInStructure"):
    for rel in wall.IsContainedInStructure:
        if rel.is_a("IfcRelContainedInSpatialStructure"):
            spatial_element = rel.RelatingStructure
            print(f"  Zugehörig zu: {spatial_element.Name}, Typ: {spatial_element.is_a()}")

print("\n-- Ende der Wandinformationen --")
