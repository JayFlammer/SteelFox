import ifcopenshell


def load_ifc_data(file_path):
    """
    Lädt eine IFC-Datei und gibt das Modell zurück.
    :param file_path: Pfad zur IFC-Datei
    :return: IFC Modell
    """
    return ifcopenshell.open(file_path)
