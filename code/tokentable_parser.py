#"./test/test4.o"
def readTokenTable(path :str, ) -> str :
    with open(path, "r", encoding="utf-8") as f:
        return_str = ""
        for line in f.readlines():
            return_str += line


    return return_str

def parseTokenTable(token_str:str) -> list:
    state = "end_tuple"
    temp_index = 0;
    return_list = []

    for index, c in enumerate(token_str):
        if c == '(' and state == 'end_tuple' :
            state = "start_tuple"
            temp_index = index + 1
        elif c == ')' and state == 'start_tuple' and token_str[index+1] != "'":
            state = 'end_tuple'
            text = token_str[temp_index:index]
            text.replace("\'","")
            return_list.append((text.split(',')[0][1:-1],text.split(',')[1][2:-1]))

    return return_list




