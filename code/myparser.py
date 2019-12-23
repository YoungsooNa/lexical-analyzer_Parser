import json
import getDataFromDefinition
from collections import deque
from tokentable_parser import parseTokenTable, readTokenTable

def parser(output_file):

    # init
    parsing_table = {}
    terminals = getDataFromDefinition.getTerminals("./definition/Terminals")
    nonTerminals = getDataFromDefinition.getTerminals("./definition/NonTerminals")
    typedef = getDataFromDefinition.getTypedef("./definition/Typedef")
    stack = []
    input_string = deque()
    input_type = deque()

    #getting parsing table
    with open("./parsing_table.json", "r", encoding="utf-8") as json1_file:
        json_str = json1_file.read()
        parsing_table = json.loads(json_str)

    #load token table
    token_table = parseTokenTable(readTokenTable(output_file))

    #make input queue
    for tuple_token in token_table:
        input_string.append(tuple_token[1])
        input_type.append(typedef[tuple_token[0]])

    # add end sign
    input_string.append('$')
    input_type.append('$')
    stack.append('$')
    stack.append('CODE')

    # loop until stack has only $
    while(len(stack) > 1):
        stack_pop = stack.pop()
        input_type_pop = input_type[0]

        # if stack_pop = epsilon skip
        if stack_pop == 'epsilon':
            continue

        # if stack_pop == input_type[0](must terminal) then remove both
        if stack_pop == input_type[0]:
            input_type.popleft()
            input_string.popleft()
            continue

        # if there is no key for parsing table print error
        if not(stack_pop in parsing_table.keys()):
            print("error occur!!!!!!!!! Stack pop : " + stack_pop + " input type : " + input_type_pop + " /// remain string : " + str(input_string))
            return False
        # get expression from parsing table
        exp = parsing_table[stack_pop][input_type_pop]

        # if nonterminal + terminal have no value in parssing table  then print error
        if exp == 0:
            print("error occur!!!!!!!!! Stack pop : " + stack_pop + " input type : " + input_type_pop + " /// remain string : " + str(input_string))
            return False

        # expression to words and add each word to stack by reverse order
        nts = exp.split("-> ")[1].split(" ")
        nts = nts[::-1]
        stack.extend(nts)
        #print("stack: " + str(stack) + " applying rule : " + exp)

    return True


# main code for testing
if __name__ == "__main__":
    result = parser("./test/test5.o")
    if result :
        print("Code is correct")
    else :
        print("Code is not correct")
