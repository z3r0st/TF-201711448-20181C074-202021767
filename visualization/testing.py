def commonStreet(streets1, streets2):
    for street in streets1:
        if street in streets2:
            return True
    return False