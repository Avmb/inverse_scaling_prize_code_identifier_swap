# inverse_scaling_prize_code_identifier_swap

Code for data generation for the Inverse Scaling Prize https://github.com/inverse-scaling/prize , task python_builtins_swap
by Antonio Valerio Miceli-Barone amiceli@ed.ac.uk .

In order to generate the dataset, first install the https://github.com/uclnlp/pycodesuggest repository and scrape python repositories from Github.
For this subission we downloaded 136 repositories from the most recent snapshot of Github available on 27 Oct 2022. We did not use the normalization scripts.

After the download is complete, run filter_functions_with_docstrings.py and filter_functions_with_docstrings.py to generate the dataset. We arbitrary cut off the dataset at 1000 examples.
This code depends on astunparse 1.6.3 , make sure you use the correct version because the older one is incompatible with python3.8 .

Special acknowledgment to Fazl Barez and the Edinburgh EA group who let me know about the Inverse Scaling Prize even though we were not able to complete a team submission.

## Task description

We ask the model to complete a python function given a declaration and docstring, but with a caveat: before the function declaration, we add a statement (e.g. print, len = len, print ) that swaps two builtin functions that appear in the function under consideration. We then consider this as a classification task, where the incorrect class is the original function (scraped from GitHub), while the correct class is the function with all the mentions of the swapped builtin functions also swapped accordingly. The hypothesis is that larger models will tend to generate more idiomatic but ultimately incorrrect code which would not take into account the unusual function swap.

## Why is the task important?

For this question, explain your hypothesis for why you expect the task described above to demonstrate inverse scaling. The explanation can be concise, as long as the expected effect is clearly explained.

Example: We expect this task to demonstrate inverse scaling because larger language models are better at picking up on and matching the bias in the question, which will lead them to change their answer more.

## Why do you expect to see inverse scaling?

Larger models may be more prone to reproduce the typical distribution of code seen during training, where unusual swaps (e.g. print with len) are normally not present.

## Why is the task novel or surprising?

Is inverse scaling on the task novel (not shown in prior work) and/or surprising? Why or why not?

## Dataset generation procedure

1. We scrape python code from github using https://github.com/uclnlp/pycodesuggest 
2. We extract top-level functions with a docstring 
3. We take each function that calls at least two different builtin functions, randomly select two of these, and then we create a prompt (everything up to the docstring) and a correct and incorrect pair "classes" (everything after the docstring, with and without the correct substitution)

# Results

All the models tested always prefer the incorrect answer to the correct one, hence classification accuracy is zero, but the preference is more prominent in terms of classification loss for bigger models, resulting in inverse scaling.
