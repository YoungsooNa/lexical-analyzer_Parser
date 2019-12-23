import getDataFromDefinition
import getFirst
import getFollow
import json

# check expression can be epsilon
def can_be_epsilon(exp:str, terminals:list, cfg:dict):
    if exp == 'epsilon':
        return True
    splited = exp.split(" ")
    for elm in splited:
        if elm in terminals:
            return False
        one_of_case = False
        for exp2 in cfg[elm] :
            if can_be_epsilon(exp2, terminals, cfg):
                one_of_case = True
        if one_of_case == False:
            return False
    return True

# get first set from expression constructed by nonterminals + terminals
def get_first_exp(exp:str, terminals:list, first:dict):
    return_first = []
    splited = exp.split(" ")
    for elm in splited:
        if elm in terminals :
            if not(elm in return_first):
                return_first.append(elm)
            break
        elif elm == 'epsilon':
            if not ('epsilon' in return_first):
                return_first.append(elm)
                continue
        for f_elm in first[elm] :
            if not(f_elm in return_first):
                return_first.append(f_elm)
        if not('epsilon' in first[elm]):
            break

    return return_first




if __name__ == '__main__' :
    # get terminals and nonTerminals and cfg from definition
    terminals = getDataFromDefinition.getTerminals("./definition/Terminals")
    nonTerminals = getDataFromDefinition.getTerminals("./definition/NonTerminals")
    cfg = getDataFromDefinition.getCFG("./definition/CFGForLL1Parser")
    # get first set and follow set
    first = getFirst.getFirst(terminals, nonTerminals, cfg)
    follow = getFollow.getFollow(terminals, nonTerminals, cfg, first, 'CODE')


    table = {}

    #init table
    for nonTerminal in nonTerminals :
        table[nonTerminal] = {}
        for terminal in terminals :
            table[nonTerminal][terminal] = 0
        table[nonTerminal]['$'] = 0

    """
        1) A -> exp
        for a in First(exp) -> M[A, a] = A -> exp
        2) if exp => epsilon then
        for b in Follow(A) M[A, b] = A -> exp
    """

    # LL(1) parsing table rule -> dictionary
    for nonTerminal in nonTerminals:
        for exp in cfg[nonTerminal]:
            # rule 1
            exp_first = get_first_exp(exp, terminals, first)
            if len(exp_first) > 0:
                for f_elm in exp_first:
                    if f_elm == 'epsilon':
                        continue
                    table[nonTerminal][f_elm] = nonTerminal + " -> " + exp
            # rule 2
            if can_be_epsilon(exp, terminals, cfg) :
                for term in follow[nonTerminal]:
                    table[nonTerminal][term] = nonTerminal + " -> " + exp


    """
    #making parsing table to csv file
    import csv
    column_names = terminals.copy()
    column_names.insert(0, "table")
    print(column_names)
    with open("parsingtable.csv", 'w', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(column_names)
        for nonTerminal in nonTerminals:
            data_list = [nonTerminal]
            for terminal in terminals:
                exp = table[nonTerminal][terminal]
                if exp == 0:
                    data_list.append("")
                else :
                    data_list.append(exp)
            writer.writerow(data_list)
    """

    #parsing table -> JSON
    json = json.dumps(table)
    f = open("parsing_table.json", "w")
    f.write(json)
    f.close()






