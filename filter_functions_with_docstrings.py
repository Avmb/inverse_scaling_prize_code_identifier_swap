#! /usr/bin/env python3

import sys
import ast
import astunparse

def usage():
    print("Usage:", file=sys.stderr)
    print("%s < file_list > functions_with_docstrings" % sys.argv[0], file=sys.stderr)
    sys.exit(-1)

def process_file(filename):
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
                    print(func_str)
                    print("###")

    except Exception:
        print("Can't process file: %s , skipping" % filename)

def main():
    if (len(sys.argv) != 1):
        usage()

    for filename in sys.stdin:
        process_file(filename.strip())

if __name__ == "__main__":
    main()

