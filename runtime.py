import random 
import os
import sys
import re
import tokenize
from io import BytesIO




def HaltSignal():
        return BaseException, sys.exit(1)

class Interpreter:
        def __init__(self, debug=False):
                self.str = str
                self.int = int
                self.float = float
                self.rastgele = random
                self.oku = lambda x: '"'+input(x)+'"'
                self.sırala = sorted
                
                

        def set_var(self, name, value):
                try: exec(f"self.{name} = {value}")
                except SyntaxError:
                        custom_output(f"Invalid Name or Value: {name}/ {value}", debug=debug)
                        return HaltSignal()
                
        def read_var(self, name):
                try: return eval(f"self.{name}")
                except: 
                        return HaltSignal()
                        
        def fooish_eval(self, text):
                for proh in ["not", "in", "is", "and", "or"]:
                        if " self."+proh+" " in text:
                                text = text.replace(" self."+proh+" ", " "+proh+" ")
                try: return eval(text)
                except NameError as ne:
                        var_name = re.findall(r"'([^']*)'", str(ne))[0]
                        return eval(text.replace(var_name, "self."+var_name)),
                        
                
                        
        def tokenizer(self, line):
                bytes = BytesIO(line.strip().encode('utf-8')).readline
                tokenized = [i.string for i in tokenize.tokenize(bytes)]
                proh = ['utf-8', '']
                for i in tokenized:
                        if i in proh or len (i.strip())<1:
                                tokenized.remove(i)
                tokenized.pop()
                #print(tokenized)
                return tokenized

def custom_output(text, newline=True, debug=False):
        if debug:
                if newline: print("-"*30+"\n"+text.strip())
                else: print(text.strip())
        
def var_names(line):
        char = "" 
        vars = []
        proh = [" ","", "not", "in", "is", "and", "or"]   #??? test
        for i in line+" ":
                if i.isalpha():
                        char += i
                else:
                        vars.append(char)
                        char=""
        vars = " ".join(vars).split()
        for i in vars:
                if i.strip() in proh:
                        vars.remove(i)
        vars = " ".join(vars).split()
        return vars 

def find_string(string):
        try:
                ind = min(string.index('"'), string.index("'"))
                rind = max(string.rindex('"'), string.rindex("'"))
                return string[ind:rind+1]
        except: return string
        

def execute_backend(code, debug=False):
        session = Interpreter(debug=debug)
        line = 0
        break_condition = True
        if code[0].strip().lower() != "başla":
                custom_output("Error: Missing starting statement", debug=debug) 
                return 1
        exec_else = False
        while break_condition:
                try:
                        line_exec = session.tokenizer(code[line])
                        if exec_else:
                                if line_exec[0].lower() == "değilse":
                                        line_exec = line_exec[1:]
                                exec_else = False
                                        
                                
                        if line_exec[0].lower() == "eğer":
                                indexed = line_exec[1:].index("ise")
                                cond = line_exec[1:indexed+1] 
                                to_eval = " "+" ".join(cond)+" "
                                for var_name_found in var_names(to_eval):
                                        to_eval = to_eval.replace(" "+var_name_found+" ", " self."+var_name_found+" ")
                                evv = session.fooish_eval(to_eval)
                                if evv:
                                        line_exec = line_exec[indexed+2:]
                                elif "=" in line_exec:
                                        line += 1
                                        continue
                                if not evv:
                                        exec_else = True
                                        
                        if "=" in line_exec:
                                line_exec = (" "+" ".join(line_exec)+" ").split(" = ")
                                to_eval = " "+line_exec[1]
                                for var_name_found in var_names(line_exec[1]):
                                        to_eval = to_eval.replace(" "+var_name_found+" ", " self."+var_name_found+" ")
                                session.set_var(line_exec[0], session.fooish_eval(to_eval))
                                
                        if line_exec[0].lower() == "bitir":
                                break_condition = False
                                
                        elif line_exec[0].lower() == "oku":
                                to_eval = " "+" ".join(line_exec[1:])+" "
                                if "->" in to_eval:
                                        to_eval, inp = to_eval.split("->")
                                        inp = session.fooish_eval(inp) 
                                else:
                                        inp = ""
                                session.set_var(to_eval,input(inp))
                        elif line_exec[0].lower() == "ekle":
                                to_eval = " "+" ".join(line_exec[1:])+" "
                                object, listname = to_eval.split("->")
                                try: session.fooish_eval(f"self.{listname}.append({object})")
                                except:
                                        try: session.fooish_eval(f"self.{listname}.append(self.{object})")
                                        except: 
                                                custom_output("Invalid Value, Can't Append", debug=debug)
                                                HaltSignal()
                                
                        elif line_exec[0].lower() == "yaz":
                                to_eval = " "+" ".join(line_exec[1:])+" "
                                fstr = find_string(to_eval)
                                if fstr != to_eval:
                                        to_eval = to_eval.replace(fstr, "#*#")
                                for var_name_found in var_names(to_eval):
                                        to_eval = to_eval.replace(" "+var_name_found+" ", " self."+var_name_found+" ")
                                to_eval = to_eval.replace("#*#", fstr)
                                print(session.fooish_eval(to_eval.strip()))
                        elif line_exec[0].lower() == "git":
                                try: line = int(line_exec[1].lower().strip("a"))-2
                                except ValueError:
                                        try:
                                                for i in range(len(code)):
                                                        if code[i].strip() == ":"+line_exec[1]:
                                                                line = i
                                                                break
                                                continue 
                                        except: custom_output("Error: Can't find mentioned step -> {}".format(line_exec[1]), debug=debug)
                                        break
                except IndexError:
                        custom_output("Warning: Missing end statement", debug=debug)
                        break
                except NameError:
                        custom_output("Error: Incorrect Concatenation", debug=debug)
                        break
                line += 1
        if break_condition: custom_output("Terminating process...", False, debug=debug)
        else:
                custom_output("Successfully executed.", not break_condition, debug=debug)
                sys.exit(0)


def execute(code, debug=False):
        to_exec = code.strip().split("\n")
        try: execute_backend(to_exec, debug=False)
        except Exception as e:
                custom_output(e, debug=debug)
        return None
                

content = """

~


"""
    
execute(content, @)
   
    
