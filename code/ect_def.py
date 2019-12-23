def add_dict(dict, key, value):
    if key in dict.keys():
        if value in dict[key]:
            return False
        else :
            dict[key].append(value)
            return True
    else :
        dict[key] = [value]
        return True

def stripForList(l : list) :
    for index, elm in enumerate(l) :
        l[index] = elm.strip()

    return l