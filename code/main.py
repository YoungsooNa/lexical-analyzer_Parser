import lexicalAnalyzer
import sys
import myparser

if __name__ == "__main__" :
    #argv like "./test/test6.c"
    file_name_full = sys.argv[1]
    file_name = ""
    if file_name_full.find(".",2) != -1:
        file_name = file_name_full[0 : file_name_full.find(".",2)]
    else :
        file_name = file_name_full
        file_name_full += ".c"

    # do lexer
    lexicalAnalyzer.main(file_name_full)
    # check correctness
    result = myparser.parser(file_name + '.o')
    if result:
        print("Code is correct")