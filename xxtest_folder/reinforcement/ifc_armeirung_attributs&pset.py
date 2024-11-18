import ifcopenshell

# Pfad zur IFC-Datei (Bitte Pfad anpassen)
ifc_file_path = r"C:\Users\FLJ\OneDrive - Halter AG\Dokumente\2.01_HSLU DC\3. Semester\DT_Progr\Modelle\Bewehrung\Decke\MET_TRW_GRO_098-BEW-BP-ET01_B_Bewehrung Vertiefungen ET1.ifc"

# IFC-Modell laden
model = ifcopenshell.open(ifc_file_path)

# Liste der Armierungselementtypen, die wir suchen
reinforcement_types = ["IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor"]

# Set für Attribute und PropertySets initialisieren, um Duplikate zu vermeiden
attributes_set = set()
property_sets = {}

# Durchlaufe alle Elemente im Modell, die zu den Armierungstypen gehören
for reinforcement_type in reinforcement_types:
    reinforcements = model.by_type(reinforcement_type)
    
    for reinforcement in reinforcements:
        # Standard Attribute erfassen
        attributes = reinforcement.get_info()
        attributes_set.update(attributes.keys())

        # PropertySets erfassen
        if hasattr(reinforcement, 'IsDefinedBy'):
            for definition in reinforcement.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition

                    # Prüfen, ob das PropertySet ein IfcPropertySet ist
                    if property_set.is_a("IfcPropertySet"):
                        if property_set.Name not in property_sets:
                            property_sets[property_set.Name] = set()

                        # Alle Eigenschaften im PropertySet erfassen
                        for prop in property_set.HasProperties:
                            if prop.is_a("IfcPropertySingleValue"):
                                property_sets[property_set.Name].add(prop.Name)

# Ausgabe der Übersicht
print("\n-- Übersicht aller Attribute --")
for attribute in sorted(attributes_set):
    print(f"- {attribute}")

print("\n-- Übersicht aller PropertySets und deren Eigenschaften --")
for pset_name, props in property_sets.items():
    print(f"\nPropertySet Name: {pset_name}")
    for prop in sorted(props):
        print(f"  - {prop}")

print("\n-- Ende der Übersicht --")
