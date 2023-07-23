# The Larger They Are, the Harder They Fail: Language Models do not Recognize Identifier Swaps in Python

Code for data generation and evaluation. Based on a submission to the Inverse Scaling Prize https://github.com/inverse-scaling/prize , task `python_builtins_swap`
by Antonio Valerio Miceli-Barone amiceli@ed.ac.uk and Fazl Barez f.barez@ed.ac.uk.
Paper: https://arxiv.org/abs/2305.15507

## Task description

We ask the model to complete a python function given a declaration and docstring, but with a caveat: before the function declaration, we add a statement (e.g. `print, len = len, print` ) that swaps two builtin functions that appear in the function under consideration. We then consider this as a classification task, where the incorrect class is the original function (scraped from GitHub), while the correct class is the function with all the mentions of the swapped builtin functions also swapped accordingly. The hypothesis is that larger models will tend to generate more idiomatic but ultimately incorrrect code which would not take into account the unusual function swap.

<img src="drake_meme.png?raw=true" alt="Drake meme" width=50% height=50%>

### Why is the task important?

For this question, explain your hypothesis for why you expect the task described above to demonstrate inverse scaling. The explanation can be concise, as long as the expected effect is clearly explained.

Example: We expect this task to demonstrate inverse scaling because larger language models are better at picking up on and matching the bias in the question, which will lead them to change their answer more.

### Why do you expect to see inverse scaling?

Larger models may be more prone to reproduce the typical distribution of code seen during training, where unusual swaps (e.g. print with len) are normally not present.

### Why is the task novel or surprising?

Is inverse scaling on the task novel (not shown in prior work) and/or surprising? Why or why not?

### Dataset generation procedure

1. We scrape python code from GitHub using https://github.com/uclnlp/pycodesuggest 
2. We extract top-level functions with a docstring 
3. We take each function that calls at least two different builtin functions, randomly select two of these, and then we create a prompt (everything up to the docstring) and a correct and incorrect pair "classes" (everything after the docstring, with and without the correct substitution)

## Code generation

In order to generate the dataset, first clone the pycodesuggest repository in the `gen_data` directory and scrape python repositories from GitHub.
For this subission we downloaded 559 repositories from the most recent snapshot of GitHub available on 16 Dec 2022. 

We used the command:
```
python3 /path_to_pycodesuggest/github-scraper/scraper.py --mode new --outdir=/full_path_to_scrape_output_dir/scrape/ --dbfile=//full_path_to_scrape_output_dir/cloned_repos.dat --githubuser=amiceli --search="CC-BY-4.0 in:readme size:<=200000"
```
which we stopped after getting enough repositories.
We did not use the normalization scripts.

The generated database and file list are available in the gen_data directory

After the download is complete, run `filter_functions_with_docstrings_and_shuffle.py` and `generate_examples.py` to generate the dataset. We arbitrary cut off the dataset at 1000 examples. Run `generate_examples_no_builtins.py` to generate the alternate dataset where non-builtin functions are swapped. Both datasets are available in the `cc_4_0_licensed/` directory.
This code depends on `astunparse 1.6.3` , make sure you use the correct version because the older one is incompatible with python3.8 .

## Evaluation

For our main experiments, clone our modified version of the Inverse Scaling Prize repository `inverse-scaling-eval-pipeline` and follow the instructions. The `experiments/` directory contains a jupyter notebook to generate the plots in the paper.

For our experiments on the Chat LLMs, use the jupyter notebook in the `eval_chat_llms/` directory.

## Results

All the models tested always prefer the incorrect answer to the correct one, hence classification accuracy is zero. For some model families the preference is more prominent in terms of classification loss for bigger models, resulting in inverse scaling.

![Main experimental results](experiments/all_models_loss_plot.png?raw=true "Main experimental results")

Similar results are observed on the Chat LLMs in the OpenAI family and Anthropic family.

![Chat LLMs results](eval_chat_llms/chat_llms_classsification_plot.png?raw=true "Chat LLMs results")

Inverse scaling is also observed when swapping non-builtin top-level functions.

![Non-builtin experiment results](experiments/non_builtins_gpt3_loss_plot.png?raw=true "Non-builtin experiment results")

LLMs prefer incorrect programs that use functions in a common way to out-of-distribution but correct programs.

## Copyright takedown

If you believe that material you own a copyright to has been included into our dataset and you wish it to be removed, please contact the authors by opening an issue on this GitHub repository.

## Cite this work

Please cite this work as:
```
@inproceedings{miceli-barone-etal-2023-larger,
    title = "The Larger they are, the Harder they Fail: Language Models do not Recognize Identifier Swaps in Python",
    author = "Miceli Barone, Antonio Valerio  and
      Barez, Fazl  and
      Cohen, Shay B.  and
      Konstas, Ioannis",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2023",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-acl.19",
    pages = "272--292",
}
```
