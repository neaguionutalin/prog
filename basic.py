from sys import *

tokens = []

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data

def lex(filecontents):
    tok = ""
    state = 0
    expr = ""
    isexpr = 0
    n = ""
    string = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1 :
                tokens.append("EXPR:" + expr)
                expr = ""
                isexpr = 0
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tok = ""
        elif  tok == "print" or tok == "PRINT":
            tokens.append("PRINT")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state ==1:
                tokens.append("STRING:" + string + "\"")
                string = "" 
                state =0
                tok = "" 
        elif state == 1: 
            string += tok
            tok = "" 
        
    print(tokens)
    return tokens
    
        
        
def parse(toks):
    i = 0
    while(i<len(toks)):
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING":
            print(toks[i+1][7:])
        i += 2
        
def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
run()