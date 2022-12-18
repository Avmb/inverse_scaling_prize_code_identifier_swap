#! /usr/bin/env python3

import sys
import random
import ast
import astunparse

def usage():
    print("Usage:", file=sys.stderr)
    print("%s < file_list > functions_with_docstrings" % sys.argv[0], file=sys.stderr)
    sys.exit(-1)

def process_file(filename, acc):
    try:
        with open(filename) as in_fs:
            file_str = in_fs.read()
            file_ast = ast.parse(file_str)
            for node in file_ast.body:
                if isinstance(node, ast.FunctionDef):
                    docstr = ast.get_docstring(node)
                    if docstr == None:
                        continue
                    func_str = astunparse.unparse(node).strip()
                    acc.append(func_str)
                    #print(func_str)
                    #print("###")

    except Exception:
        print("Can't process file: %s , skipping" % filename, file=sys.stderr)

def main():
    if (len(sys.argv) != 1):
        usage()

    acc = []
    for filename in sys.stdin:
        process_file(filename.strip(), acc)
    
    random.shuffle(acc)
    print("\n###\n".join(acc))


if __name__ == "__main__":
    main()

