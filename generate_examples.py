#! /usr/bin/env python3

import sys
import ast
import astunparse
import builtins
import random
random.seed(42)
import copy

def usage():
    print("Usage:", file=sys.stderr)
    print("%s max_num_examples < functions_with_docstrings > examples" % sys.argv[0], file=sys.stderr)
    sys.exit(-1)

def output_csv(prompt, bad_class, good_class):
    prompt_str = '"' + prompt.replace('"', '""') + '"'
    #classes_str = '"' + repr([bad_class, good_class]).replace('"', '""').replace("\\n", "\n") + '"'
    bad_class =  ('""" '+ bad_class+'\n"""').replace('"', '""')
    good_class = ('""" '+good_class+'\n"""').replace('"', '""')
    classes_str = '"['+bad_class+", "+good_class+']"'
    idx_str = "1"

    csv_line = ','.join([prompt_str, classes_str, idx_str])
    print(csv_line)

def generate_example(found_func_names, func_node):
    #print("%s: %s" % (func_node.name, list(found_func_names)))
    
    # Randomly choose two builtin functions
    found_func_names = sorted(list(found_func_names))
    random.shuffle(found_func_names)
    f0, f1 = found_func_names[:2]

    # swap statement
    swap_statement_str = "%s, %s = %s, %s" % (f0, f1, f1, f0)

    # bad (unmodified) function
    bad_func = astunparse.unparse(func_node).strip()
    bad_func_lines = bad_func.split("\n")

    # good function with swapped builtins
    good_func_node = copy.deepcopy(func_node)
    def traverse(node):
        if isinstance(node, ast.Name):
            if node.id == f0:
                node.id = f1
            elif node.id == f1:
                node.id = f0
        for child in ast.iter_child_nodes(node):
            traverse(child)
    traverse(good_func_node)
    good_func = astunparse.unparse(good_func_node).strip()
    good_func_lines = good_func.split("\n")

    #print(f0, f1)
    #print(swap_statement_str)
    #print(bad_func)
    #print(good_func)

    # find docstring line
    docstring_repr = repr(ast.get_docstring(func_node, clean=False))
    for i, line in enumerate(bad_func_lines):
        if line.strip() == docstring_repr:
            docstring_line_num = i
            break

    # prepare prompt
    pretty_docstring = '    """' + ast.get_docstring(func_node, clean=False) + '"""'
    prompt_lines = [swap_statement_str] + bad_func_lines[:docstring_line_num] + [pretty_docstring]
    prompt = "\n".join(prompt_lines)
    #print(prompt)

    # bad class
    bad_class = "\n" + "\n".join(bad_func_lines[docstring_line_num+1:])
    #print(bad_class)

    # good class
    good_class = "\n" + "\n".join(good_func_lines[docstring_line_num+1:])
    #print(good_class)

    # output csv
    output_csv(prompt, bad_class, good_class)

target_func_names = set([x for x in dir(builtins) if callable(eval(x))])

num_generated_funcs = 0

def process_function(func_node):
    # find calls to two builtin functions
    global num_generated_funcs

    found_func_names = set()
    def traverse(node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in target_func_names:
            found_func_names.add(node.func.id)
        for child in ast.iter_child_nodes(node):
            traverse(child)
    traverse(func_node)

    # num of builtins check
    if len(found_func_names) < 2:
        return
    func_str = astunparse.unparse(func_node).strip()
    # length check
    if len(func_str.split()) > 200:
        return
    # special char check
    if ('"""' in func_str) or ('\\\n' in func_str):
        return

    # suitable function
    generate_example(found_func_names, func_node)
    num_generated_funcs += 1

def process(max_num_examples):
    file_str = sys.stdin.read()
    file_str = file_str.replace('\x00','').strip()
    functions = [f.strip() for f in file_str.split("###\n")]
    for f in functions:
        if num_generated_funcs >= max_num_examples:
            break
        try:
            func_node = ast.parse(f)
        except SyntaxError:
            continue
        for node in func_node.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            process_function(node)
    print("Number of examples: %s" % num_generated_funcs, file=sys.stderr)

def main():
    if (len(sys.argv) != 2):
        usage()

    # print csv preamble
    print("prompt,classes,answer_index")

    process(int(sys.argv[1]))

if __name__ == "__main__":
    main()

