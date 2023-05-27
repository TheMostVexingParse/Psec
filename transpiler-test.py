import re


static_template = """

using System;
using System.Collections;
using System.Collections.Generic;


namespace PsecTranspiled {{
    class Psec {{
        static void Main(string[] args) {{
        
{}

        }}
    }}
}}

"""

default_indent      = "            "
tab_indent          = "    "


def process_line(line):
    line = line.split("//")[0].strip()


    line = re.sub("'([^\"]*)'", r'"\1"', line)

    isdef = re.findall(r'[^=]=[^=]', line)



    if line == '':
        return
    
    elif line.startswith('başla') or line.startswith('bitir'):
        return
    
    elif line.startswith(':'):
        return default_indent+line[1:]+':'
    
    elif line.startswith('yaz'):
        analyzed = native_transform(re.findall(r"yaz\s+(.*)", line)[0])
        line = 'Console.WriteLine({});'.format(analyzed)

    elif line.startswith('git'):
        line = re.sub(r'git\s+(.*)', r'goto \1;', line)

    elif line.startswith('eğer'):
        expression = re.findall(r'eğer\s+(.*)', line)[0]
        logical_expression, statement = re.findall(r'(.*)\s+ise\s+(.*)', expression)[0]
        logical_expression = native_transform(logical_expression)
        statement = process_line(statement)
        
        line = f'if ({logical_expression}) {{\n{tab_indent+statement}\n{default_indent}}}'

    elif line.startswith('değilse'):
        expression = re.findall(r'değilse\s+(.*)', line)[0]
        statement = expression.replace('değilse', '').strip()
        statement = process_line(statement)
        line = f'else {{\n{tab_indent+statement}\n{default_indent}}}'

    elif line.startswith('ekle'):
        #syntax: ekle <variable> -> <target>
        variable, target = re.findall(r'ekle\s+(.*)\s+->\s+(.*)', line)[0]
        variable = native_transform(variable)
        line = "{}.Add({});".format(target, variable)


    elif isdef:
        right_statement = native_transform(line.split("=")[-1].strip())
        line = "= ".join(line.split("=")[:-1]+[right_statement])
        line += ";"

    else:
        #needs further processing
        line = native_transform(line)
        

    return default_indent+line

def native_transform(line):
    line = line.strip()
    if line == "[]":
        line =  "new List<dynamic>()"
    #python-native type conversions
    line = re.sub(r'int(.*)', r'int.Parse(\1)', line)
    line = re.sub(r'float(.*)', r'float.Parse(\1)', line)
    
    if "oku" in line:
        var_name = line.replace("oku", "").strip()
        line = "{} = Console.ReadLine();".format(var_name)
    # if "sırala" in line:
    #     sort_object = re.findall(r'sırala(.*)', line)[0][1:-1]
    #     line = line.replace(sort_object, )
    #     print(sort_object)
    return line


def extract_variable_names(code):
    already_yielded = []
    to_yield = None
    for line in code.split('\n'):
        if len(line.strip()) > 0:
            if re.findall(r'[^=]=[^=]', line):
                to_yield = line.split('=')[0].strip()
            elif line.startswith('oku'):
                to_yield = line.replace('oku', '').strip()
            if to_yield in already_yielded:
                continue
            else:
                already_yielded.append(to_yield)
                to_yield = str(to_yield)
                if len(to_yield.split()) > 1:
                    continue
                yield to_yield


def process_code(code):
    collected = []
    for line in code.split('\n'):
        rebuilt_line = process_line(line)
        if rebuilt_line:
            collected.append(rebuilt_line)

    if collected[-1].endswith(':'):
        collected.append(default_indent+';')

    for variables in extract_variable_names(code):
        collected.insert(0, default_indent+f'dynamic {variables};')
    
    return static_template.format('\n'.join(collected))


code = """
başla

oku sayı
yaz "-----------------------------------"
yaz "çarpanlar bulunuyor"
yaz "-----------------------------------"
sayı = int(sayı)
lim = sayı/2+1
say = []
ekle sayı -> say
i = 0
col = 0

:döngü
i = i+1
eğer sayı%i == 0 ise git ekleyici
eğer i > lim ise git disp
git döngü

:ekleyici
ekle i -> say
col = col+1
git döngü

:disp
index = 0

:tekrar
yaz say[index]
eğer index < col ise index = index+1
değilse git son
git tekrar

:son
bitir
"""

result = process_code(code)
print(result)