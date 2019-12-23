import ect_def

def getTerminals(path:str)->list:
    terminals = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            terminals.append(line.replace("\n", ""))

    return terminals

def getCFG(path :str) ->list :
    cfg = {}
    with open(path, "r", encoding="utf-8") as f :
        for line in f.readlines():
            if not('->' in line):
                continue
            key = line.split('->')[0].strip()
            data = line.split('->')[1].split('|')
            cfg[key] = ect_def.stripForList(data)
    return cfg

def getTypedef(path:str) -> dict :
    typedef = {}
    with open(path, "r", encoding="utf-8") as f :
        for line in f.readlines():
            typedef[line.split('=')[1].strip()] = line.split('=')[0].strip()

    return typedef