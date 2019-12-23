"""
/*
* Writer         : YoungSoo, Na
* Program     : lexical Analyzer
* How to use : python lexicalAnalyzer.py test/filename.c
*/
"""

import sys


#definition of letter and digit
LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT = "0123456789"

# my token category based on 2019_compiler_term_project_1.pdf
# All the symbols have thier own category
token_category = {
    'identifier' : "ID",
    'int' : 'INT',
    'char' : 'CHAR',
    'digit' : 'DIGIT',
    'string' : 'STRING',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULTIFLY',
    '/': 'DIVIDE',
    '<': 'LESS',
    '>': 'GREATER',
    '==': 'EQUAL',
    '=' : "ASSIGNMENT",
    '!=': 'NOTEQUAL',
    '<=': 'LESSEQUAL',
    '>=': 'GREATEREQUAL',
    ';': 'SEMICOLON',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LCURLYBRACE',
    '}': 'RCURLYBRACE',
    ',': 'COMMA'
}
# keywords for distinguish between kewrods and identifier
KEYWORDS = ["int", "char", "if","else","while","return"]

# function for check the whitespaces to skip
def checkWHITESPACE(c:str) -> bool :
    if c == ' ' or  c == '\t' or c == '\r' :
        return True
    return False



# dfa for identifier
def dfa_id(state:int, c:str) :
    if state == 0 and c in LETTER :
        return 1
    elif state == 0 and c in DIGIT:
        return -1
    elif state == 1 and c in LETTER:
        return 2
    elif state == 1 and c in DIGIT:
        return 3
    elif state == 2 and c in LETTER:
        return 2
    elif state == 2 and c in DIGIT:
        return 3
    elif state == 3 and c in LETTER:
        return 3
    elif state == 3 and c in DIGIT:
        return 3
    else :
        return -1

# dfa for digit
def dfa_digit(state:int, c:str) :
    if state == 0 and c == '-':
        return 1
    elif state == 0 and c in "123456789" :
        return 2
    elif state == 0 and c == "0":
        return 3
    elif state == 1 and c == '-':
        return -1
    elif state == 1 and c in "123456789" :
        return 4
    elif state == 1 and c == "0":
        return 3
    elif state == 2 and c in "123456789" :
        return 4
    elif state == 2 and c == "0":
        return 3
    elif state == 1 and c == '-':
        return -1
    elif state == 4 and c in DIGIT :
        return 4
    else :
        return -1
# dfa for string
def dfa_string(state:int, c:str) :
    if state == 0 and c == "\"" :
        return 1
    elif state == 1 and (c in LETTER or c in DIGIT) :
        return 1
    elif state == 1 and c == "\"":
        return 2
    else :
        return -1

# lexer
def lexer(source_code:str):
    # it return value like ( ( ID, value) , ... ( }, RCURRYBRACE) )
    token_table:list  = []
    # state [0] for divide dfa [1] dfa using state
    state: list = [0,0]
    # Position of the currentyly processed character
    index: int = 0
    # buffer for saving string which sum of prev characters
    buffer: str = ""

    # loop until end
    while True:
        # if index out of lange or current character is \n
        if index >= len(source_code) or source_code[index] == '\n':
            break

        # if current character is whitespace skip
        if checkWHITESPACE(source_code[index]) :
            index += 1
            continue

        # if current dfa state is 0 define which dfa will be used
        if state[0] == 0:
            # reset state[1] to 0 for another dfa
            state[1] = 0
            buffer = ""
            # if start with letter will be using dfa_id
            if source_code[index] in LETTER :
                state[0] =1
            # if start with digit or - will be using dfa_digit
            elif source_code[index] in DIGIT or source_code[index] in '-':
                state[0] = 2
            # if start with " , will be using dfa_string
            elif source_code[index] == "\"":
                state[0] = 3
            # othercase will be process another code
            else :
                state[0] = 4

        else :
            if state[0] == 1:
                #using dfa_id until return -1
                while True:
                    state[1] = dfa_id(state[1], source_code[index])
                    if state[1] == -1:
                        break
                    buffer += source_code[index]
                    index += 1
                # if buffer in the KEYWORDS, process it as a keyword
                if buffer in KEYWORDS:
                    token_table.append((token_category[buffer], buffer))
                # else it is Identifier
                else :
                    token_table.append(("ID", buffer))
                #reset state
                state[0] = 0

            elif state[0] == 2:
                # using dfa_digit until it returns -1
                while True:
                    state[1] = dfa_digit(state[1], source_code[index])
                    if state[1] == -1:
                        break
                    buffer += source_code[index]
                    index += 1
                # append token_table
                token_table.append(("DIGIT",buffer))
                # reset state
                state[0] = 0

            elif state[0] == 3:
                # using dfa_string until it returns -1
                while True:
                    state[1] = dfa_string(state[1], source_code[index])

                    if state[1] == -1:
                        break

                    buffer += source_code[index]
                    index += 1
                token_table.append(("STRING", buffer))
                state[0] = 0

            elif state[0] == 4:
                # if not id, digit, string it was keywords or not defined charater
                if source_code[index] in token_category.keys():
                    buffer = source_code[index]
                    token_table.append((token_category[buffer],buffer))
                    index += 1
                    state[0] = 0
                else :
                    print("error! This is not correct character : " + source_code[index])
                    return -1

    return token_table


def main(file_name_full_arg):
    # get file_name from the arguments[1]
    #file_name_full = sys.argv[1]
    file_name_full = file_name_full_arg
    file_name = ""
    # get full of filename and filename without extender
    if file_name_full.find(".",2) != -1:
        file_name = file_name_full[0 : file_name_full.find(".",2)]
    else :
        file_name = file_name_full
        file_name_full += ".c"

    #list for save token
    token_table = []

    # open file
    with open(file_name_full, 'r', encoding='utf-8') as f:
        # read line by line 
        for line, source_code in enumerate(f.readlines(),start=1):
            # do lexer for line
            result = lexer(source_code)
            # if error occur stop working and save previous work
            if result == -1:
                print("error in line (" + str(line) + ")")
                break
            else :
                #if not error occured add result to token table
                token_table.extend(result)

    # save file "filename.o"
    with open(file_name + '.o', 'w', encoding='utf-8') as f:
        f.write(str(token_table))

    #print end of program
    print("lexer worked!")










