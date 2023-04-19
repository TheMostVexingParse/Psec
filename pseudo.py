import sys
import os
import subprocess
import py_compile


COMP = """

from distutils.core import setup
import py2exe
import sys

dll_excludes = [
                "crypt32.dll",
                "w9xpopen.exe",
                "mswsock.dll",
                "powrprof.dll",
                "mpr.dll"
                ]

excludes=['crypto', 'openssl', '_ssl', 'pyreadline', 'difflib', 'doctest', 'locale', 'optparse', 'pickle', 'calendar', 'pbd', 'unittest', 'inspect', '_tkinter', 'tkinter']
includes=['imp']
                                 
sys.argv.append("--dll-excludes=%s" % ",".join(dll_excludes))
sys.argv.append("--excludes=%s" % ",".join(excludes))
sys.argv.append("--includes=%s" % ",".join(includes))

setup(
    options = {{'py2exe': {{'optimize': 2, 'bundle_files': {}, 'compressed': {}}}}},
    console=['{}'],
    zipfile = None
)

"""


if __name__ == '__main__':
    args = sys.argv
    args[0] = args[0].split('\\')[-1]

    trace = False
    bytecode = False
    compile_ = False
    debug = False
    onefile = 3
    
    if args[0] == 'python': args.pop(0)
    if args[0] == __file__.split('\\')[-1]: args.pop(0)

    if '--bytecode' in args: args.remove('--bytecode'); bytecode = True
    if '--compile' in args: args.remove('--compile'); compile_ = True
    if '--trace' in args: args.remove('--trace'); trace = True
    if '--onefile' in args: args.remove('--onefile'); onefile= 1
    if '--debug' in args: args.remove('--debug'); debug = True

    target = False
    
    for i in args:
        if i.endswith('.pc'):
            target = i

    if not target:
        raise Exception('Invalid command formatting, input file not found.')

    if bytecode or compile_:
        with open('runtime.py', 'r', encoding = 'utf-8') as file: pholder = file.read().replace('@', str(debug))
        with open(target, 'r', encoding = 'utf-8') as file: code = file.read()

        pholder = code.join(pholder.split('~'))
        out = target.replace('.pc', '')+'.py'

        with open(out, 'w+', encoding='utf-8') as file: file.write(pholder)
        
        if compile_:
            with open('compiler.py', 'w+', encoding='utf-8') as file:
                file.write(COMP.format(str(onefile), 'True', out, out))
            result = subprocess.run(['python', 'compiler.py', 'py2exe'], stdout=subprocess.PIPE)
            os.remove('compiler.py')
        else: py_compile.compile(out)
        
        os.remove(out)
            
        
