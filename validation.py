# These are functions for the logic after coordinates input in the form

def valid_latitude(coordinate): # TO DO : FIX THIS !
    """ This function validates if the input latitude
    by the user is safe (not using any injections) and 
    the type of input latitude given is correct (only floats or integers), as well
    checks if the given range is correct."""
    try:
        float(coordinate)
    except ValueError:
        return False
    else:
        coordinate = float(coordinate)
        if coordinate <= -90 or coordinate >= 90:
            return False
        else:
            return True

def valid_longitude(coordinate):
    """ This function validates if the input longitude
    by the user is safe (not using any injections) and 
    the type of input longitude given is correct (only floats or integers), as well
    checks if the given range is correct."""
    try:
        float(coordinate)
    except ValueError:
        return False
    else:
        coordinate = float(coordinate)
        if coordinate <= -180 or coordinate >= 180:
            return False
        else:
            return True

def valid_address(address):
    """
    This input cannot be a number.
    """
    try:
        float(address)
    except ValueError:
        return True
    else:
        return False

# TO DO: Try obtaining coordinate from google maps.
# TO DO: UML diagram
