def calculate_concrete_volume(elements_data):
    """
    Berechnet das Volumen basierend auf der Dicke und Fläche der Elemente.
    :param elements_data: Liste der Elemente mit Dicke und Fläche
    :return: Gesamtes Volumen in m³
    """
    total_volume = 0.0
    for dicke, flaeche in elements_data:
        volume = dicke * flaeche
        total_volume += volume
    return round(total_volume, 2)




