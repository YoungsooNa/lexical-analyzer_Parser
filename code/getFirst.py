from ect_def import add_dict
def getFirst(terminals:list, non_terminals:list, cfg:dict) ->list :
    first = {}
    for non_terminal in non_terminals:
        unsolved_nt = [non_terminal]
        while(len(unsolved_nt) > 0) :
            nt = unsolved_nt[0]
            unsolved_nt.remove(nt)
            for result in cfg[nt]:
                first_word = result.split(' ')[0]
                if first_word in terminals or first_word == 'epsilon':
                    add_dict(first, non_terminal, first_word)
                else:
                    unsolved_nt.append(first_word)

    return first


