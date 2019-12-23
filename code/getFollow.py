from ect_def import add_dict

"""
Rules of Follow
1) if A is a nonterminal and start sign then FOLLOW(A) include $
2) if B -> aAb, b != epsilon then FOLLOW(A) include FIRST(b) without epsilon
3) if B -> aA or B -> aAb b=>epsilon then add FOLLOW(B) to FOLLOW(A)

"""

def getFollow(terminals:list, non_terminals:list, cfg:dict, first:dict, start_nonterminal:str) :
    follow = {}
    #rule 1
    add_dict(follow, start_nonterminal, "$")
    for non_terminal in non_terminals:
        # rule 2
        for cfg_result in cfg[non_terminal]:
            splited = cfg_result.split(' ')
            for index, word in enumerate(splited):
                # if word is non termianl and next word exist
                if word in non_terminals and index < len(splited)-1:
                    next_word = splited[index+1]
                    if next_word in terminals:
                        add_dict(follow, word, splited[index+1])
                    else :
                        if len(first[next_word]) == 1 and 'epsilon' in first[next_word]:
                            continue
                        else :
                            for first_elm in first[next_word]:
                                if first_elm != 'epsilon' and not(word in follow.keys() and first_elm in follow[word]):
                                    add_dict(follow, word, first_elm)
    # rule3
    include_relation = {}
    for non_terminal in non_terminals:
        for cfg_result in cfg[non_terminal]:
            splited = cfg_result.split(' ')
            for index, word in enumerate(splited):
                # if word is non termianl and word is last word then follow(word) include non_terminal
                if word in non_terminals and index == len(splited) - 1:
                    if word == non_terminal:
                        continue
                    if word in include_relation.keys():
                        if not(non_terminal in include_relation[word]) :
                            add_dict(include_relation, word, non_terminal)
                    else :
                        add_dict(include_relation, word, non_terminal)
                # if word is non termianl and word is not last word and all word's next words can be epsilon then follow(word) include non_terminal
                elif word in non_terminals and index != len(splited) - 1:
                    possible_epsilon = True
                    for i in range(index+1,len(splited)):
                        if splited[i] in terminals:
                            possible_epsilon = False
                            continue
                        if not('epsilon' in first[splited[i]]):
                            possible_epsilon = False

                    if possible_epsilon == True:
                        add_dict(include_relation, word, non_terminal)
    # add follow with include relation until no change
    while(True):
        change_count = 0
        for key in include_relation.keys():
            for value in include_relation[key]:
                if not(value in follow.keys()):
                    continue
                else:
                    for add_value in follow[value]:
                        if add_dict(follow, key, add_value):
                            change_count += 1


        if change_count == 0 :
            break


    return follow

