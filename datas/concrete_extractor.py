def concrete_extract_wall_slab_properties(model):
    try:
                # Elemente durchsuchen (IfcWall und IfcSlab)
        elements = model.by_type("IfcWall") + model.by_type("IfcSlab")

        # Ergebnipysliste initialisieren
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