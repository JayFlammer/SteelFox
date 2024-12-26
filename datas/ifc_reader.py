import ifcopenshell


def load_ifc_data(file_path):
    """
    Die erste Funktion dieses Programms :)
    """
    return ifcopenshell.open(file_path)