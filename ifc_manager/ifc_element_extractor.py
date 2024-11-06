import ifcopenshell.util.element

def extract_concrete_and_reinforcement(model):
    """
    Extrahiert Beton- und Armierungselemente aus dem IFC-Modell.
    :param model: IFC Modell
    :return: Tuple mit Listen der Beton- und Armierungselemente
    """
    concrete_elements = model.by_type('IfcWall') + model.by_type('IfcSlab')
    reinforcement_elements = model.by_type('IfcReinforcingBar')
    return concrete_elements, reinforcement_elements
