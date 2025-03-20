def merge_recursive(value1, value2):
    """Merge two dict recursive"""
    t1, t2 = type(value1), type(value2)
    if t1 != t2 or value1 == None:
        return value2
    if t2 is dict:
        out = {}
        keys = value1.keys() | value2.keys()
        for k in keys:
            if k in value1:
                if k in value2:
                    out[k] = merge_recursive(value1[k], value2[k])
                else:
                    out[k] = value1[k]
            else:
                out[k] = value2[k]
        return out
    elif t2 is set:
        return value1 | value2
    elif t2 in (list, tuple):
        return value1 + value2
    else:
        return value2
