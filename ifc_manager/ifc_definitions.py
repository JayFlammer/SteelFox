# Hier könnten allgemeine Definitionen und Konstanten festgelegt werden.

# Beispielkonstanten
IFC_CONCRETE_TYPES = ['IfcWall', 'IfcSlab']
IFC_REINFORCEMENT_TYPES = ['IfcReinforcingBar']

# Funktion zur Überprüfung, ob ein Element ein bestimmter Typ ist
def is_concrete(element):
    """
    Überprüft, ob ein Element zum Betontyp gehört.
    :param element: IFC Element
    :return: True, wenn es ein Betonelement ist, sonst False
    """
    return element.is_a() in IFC_CONCRETE_TYPES