from sys import *

tokens = []

def open_file(filename):
    data = open(filename, "r").read()
    return data

def lex(filecontents):
    tok = ""
    state = 0
    string = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            tok = ""
        elif  tok == "print":
            print("found a print")
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state ==1:
                print("found a string")
                string = "" 
                state =0
        elif state == 1: 
            string += char
            tok = "" 

        
def run():
    data = open_file(argv[1])
    lex(data)

run()
