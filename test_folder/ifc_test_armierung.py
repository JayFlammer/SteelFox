import ifcopenshell

# Pfad zur IFC-Datei (Bitte Pfad anpassen)
ifc_file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Bewehrung\Decke\MET_TRW_GRO_098-BEW-BP-ET01_B_Bewehrung Vertiefungen ET1.ifc"

# IFC-Modell laden
model = ifcopenshell.open(ifc_file_path)

# Liste der Armierungselementtypen, die wir suchen
reinforcement_types = ["IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor"]

# Durchlaufe alle Elemente im Modell, die zu den Armierungstypen gehören
for reinforcement_type in reinforcement_types:
    reinforcements = model.by_type(reinforcement_type)
    
    for reinforcement in reinforcements:
        print(f"\nElement ID: {reinforcement.GlobalId}, Typ: {reinforcement.is_a()}\n")

        # Ausgabe aller Standardattribute des Elements (z.B. IfcReinforcingBar)
        print("-- Standard Attribute --")
        attributes = reinforcement.get_info()  # Diese Methode liefert ein Dictionary mit allen Attributen
        for attr_name, attr_value in attributes.items():
            print(f"{attr_name}: {attr_value}")

        # Alle Beziehungen (z.B. zu PropertySets) auslesen
        print("\n-- Beziehungen und PropertySets --")
        if hasattr(reinforcement, 'IsDefinedBy'):
            for definition in reinforcement.IsDefinedBy:
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

        if hasattr(reinforcement, 'Representation') and reinforcement.Representation:
            representation = reinforcement.Representation

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

print("\n-- Ende der Armierungselemente --")