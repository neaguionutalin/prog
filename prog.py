from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data

def lex(filecontents):
    tok = ""
    state = 0
    expr = ""
    isexpr = 0
    var = ""
    varstarted = 0
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
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            elif tokens[-1] == "LESS":
                tokens[-1] = "LESSEQUAL"
            elif tokens[-1] == "MORE":
                tokens[-1] = "MOREEQUAL"
            else:
                tokens.append("EQUALS")
            tok = ""
        elif tok == "<" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("LESS")
            tok = ""
        elif tok == "to" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("TO")
            tok = ""
        elif tok == "TO" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("TO")
            tok = ""
        elif tok == ">" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("MORE")
            tok = ""
        elif tok == "!=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("NOTEQUAL")
            tok = ""
        elif tok == "$" and state == 0:
            varstarted = 1
            var += tok
            tok = ""
        elif varstarted ==1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varstarted = 0
            var += tok
            tok = ""
        elif  tok == "print" or tok == "PRINT":
            tokens.append("PRINT")
            tok = ""
        elif  tok == "input" or tok == "INPUT":
            tokens.append("INPUT")
            tok = ""
        elif  tok == "if" or tok == "IF":
            tokens.append("IF")
            tok = ""
        elif tok == "elif" or tok == "ELIF":
            tokens.append("ELIF")
            tok = ""
        elif tok == "else" or tok == "ELSE":
            tokens.append("ELSE")
            tok = ""
        elif tok == "for" or tok == "FOR":
            tokens.append("FOR")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\t":
            tok = ""
        elif tok == "\"" or tok == " \"":
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

    if tokens[-1] == "LESS":
        del tokens[-1]
    #print(tokens)
    return tokens
    #return ''


def evalExpression(expr):
    return eval(expr)

def doPRINT(toPRINT):
    if toPRINT[0:6] == "STRING":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    if toPRINT[0:3] == "NUM":
        toPRINT = toPRINT[4:]
    if toPRINT[0:4] == "EXPR":
        toPRINT = evalExpression(toPRINT[5:])
    print(toPRINT)

def doASSIGN(varname, varvalue):
    symbols[varname[4:]]=varvalue

def getVARIABLE (varname):
    varname = varname[4:]
    if varname in symbols:

        return symbols[varname]
    else:
        return "VARIABLE ERROR: Undefined Variable"
        exit()

def getINPUT (string, varname):
    i = input(string[1:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""


def parse(toks):
    i = 0
    ifc = 0
    #ifc -> 0 not in if or if true
    #ifc -> 1 if false

    while(i<len(toks)):
        if toks[i] == "FOR":
            i+=1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM TO NUM":
                a = int(toks[i][4:])
                b = int(toks[i+2][4:])
            elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR TO VAR":
                a = getVARIABLE(tok[i])
                b = getVARIABLE(tok[i+2])
            elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM TO VAR":
                a = int(toks[i][4:])
                b = getVARIABLE(toks[i+2])
            elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR TO NUM":
                a = getVARIABLE(toks[i])
                b = int(toks[i+2][4:])
            else:
                print("Error: False definition of for")
                exit()
            i+=3
            b+=1
            if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
                for x in range(a,b):
                    if toks[i+1][0:6] == "STRING":
                        doPRINT(toks[i+1])
                    elif toks[i+1][0:3] == "NUM":
                        doPRINT(toks[i+1])
                    elif toks[i+1][0:4] == "EXPR":
                        doPRINT(toks[i+1])
                    elif toks[i+1][0:3] == "VAR":
                        doPRINT(getVARIABLE(toks[i+1]))
            i += 2
            if len(toks) == i:
                exit()
    #need to add what the for will do, repeatedly

        if toks[i] == "IF":
            ifc = 1
            i+=1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM EQEQ NUM":
                if toks[i][4:] == toks[i+2][4:]:
                    ifc = 0
                if toks[i][4:] != toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQEQ VAR":
                if getVARIABLE(toks[i]) == getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) != getVARIABLE(toks[i+2]):
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM LESS NUM":
                if toks[i][4:] < toks[i+2][4:]:
                    ifc = 0
                elif toks[i][4:] > toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR LESS VAR":
                if getVARIABLE(toks[i]) < getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) > getVARIABLE(toks[i+2]):
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM MORE NUM":
                if toks[i][4:] > toks[i+2][4:]:
                    ifc = 0
                elif toks[i][4:] < toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR MORE VAR":
                if getVARIABLE(toks[i]) > getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) < getVARIABLE(toks[i+2]):
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM LESSEQUAL NUM":
                if toks[i][4:] <= toks[i+2][4:]:
                    ifc = 0
                elif toks[i][4:] > toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR LESSEQUAL VAR":
                if getVARIABLE(toks[i]) <= getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) > getVARIABLE(toks[i+2]):
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM MOREEQUAL NUM":
                if toks[i][4:] >= toks[i+2][4:]:
                    ifc = 0
                elif toks[i][4:] < toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR MOREEQUAL VAR":
                if getVARIABLE(toks[i]) >= getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) < getVARIABLE(toks[i+2]):
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "NUM NOTEQUAL NUM":
                if toks[i][4:] != toks[i+2][4:]:
                    ifc = 0
                elif toks[i][4:] == toks[i+2][4:]:
                    ifc = 1
            if toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR NOTEQUAL VAR":
                if getVARIABLE(toks[i]) != getVARIABLE(toks[i+2]):
                    ifc = 0
                if getVARIABLE(toks[i]) == getVARIABLE(toks[i+2]):
                    ifc = 1
            i+=3
        if ifc == 0:
            if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
                if toks[i+1][0:6] == "STRING":
                    doPRINT(toks[i+1])
                elif toks[i+1][0:3] == "NUM":
                    doPRINT(toks[i+1])
                elif toks[i+1][0:4] == "EXPR":
                    doPRINT(toks[i+1])
                elif toks[i+1][0:3] == "VAR":
                    doPRINT(getVARIABLE(toks[i+1]))
                i += 2
            elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
                if toks[i+2][0:6] == "STRING":
                    doASSIGN(toks[i], toks[i+2])
                elif toks[i+2][0:3] == "NUM":
                    doASSIGN(toks[i], toks[i+2])
                elif toks[i+2][0:4] == "EXPR":
                    doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:])))
                elif toks[i+2][0:3] == "VAR":
                    doASSIGN(toks[i], getVARIABLE(toks[i+2]))
                i+=3
            elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
                getINPUT(toks[i+1][7:],toks[i+2][4:])
                i+=3
        if ifc == 1:
            if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
                i += 2
            elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
                i+=3
            elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
                i+=3
    #print(symbols)



def run():
    filename = ""
    filename = input("what is the name of you file? (Please include the extension as well) ")
    data = open_file(filename)
    toks = lex(data)
    parse(toks)
run()
