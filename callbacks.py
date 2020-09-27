def is_int_callback(val):
    if val == '':
        return True
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float_callback(val):
    if val == '':
        return True
    try:
        float(val)
        return True
    except ValueError:
        return False
