# digraph-kings-study
a computational study on king-vertices in products of directed graphs; the products of interest are Cartesian, strong, 
lexicographic, and direct-- the last of which is the main focus of this project; the inspiration of this project draws
heavily from [1]

## purpose
this project aims to identify how king-vertices in the factors of direct products affect the existence of kings in the
product; it's generally understood how king-vertices in the factors of cartesian, strong, and lexicographic products 
affect kings in each of their respective products; in direct products this is less understood, thusly we hope to
identify properties of factor graphs that lead to specific characteristics in their direct products, and possibly 
vice-versa

## findings

this project produced two theorems characterizing when kings exist in the direct product of two tournaments:

**Theorem 1.** Let `T` be an `(n, k)`-tournament and `T'` be an `(n', k')`-tournament. Then `T × T'` has `k · k'` kings if and only if `k, k' ≠ 1`, and at least one of `k, k' ≥ 4`, with `n, n' > 1`.

**Theorem 2.** Let `T` be an `n`-tournament and `T'` be an `n'`-tournament, and let `T × T'` be the direct product of `T` and `T'`. If `(v, v')` is a `k`-king in `T × T'`, then `k ≥ 3`, where `v` is a king in `T`, `v'` is a king in `T'`, and `n' > 1`.

these results came out of an exhaustive computational search over every tournament up to order 10, generating all direct products between tournament pairs and checking the resulting graphs for king-vertices. the results informed both the necessary conditions in Theorem 2 and the tighter characterization in Theorem 1.

these findings are still under supervisor review and have not yet been submitted for publication.

## technologies-used
- `Python 3.12`; chosen for ease of work, and available packages
- `NetworkX`; https://networkx.org/

## usage

### requirements

- `Python 3.12`
- `NetworkX` (<https://networkx.org/>)

install NetworkX with:

```bash
pip install networkx
```

### running the search

NOTE: the required tournament files are provided within this repository, within the `projectFiles/digraph_datasets/t_files` 
directory. you will need to extract `tourn10.txt` file from its gzip in order to proceed - the unzipped file is about 400MB

1. Select the tournament order, and the specific line (pinpointing a specific tournament within that order's file) that you'd like to take the direct product of against all other tournaments.

2. Within `projectFiles/main.py`, edit the line that calls the experimental function `min_max_k_val_kings_experiment()`. It takes two arguments, `specified_order` and `specified_line` — fill these in with what you selected in step 1.

3. Run the script, either through a CLI or through your IDE of choice.

WARNING: due to the number of tournament combinations, this script will take quite a long time to run to completion!

Keep an eye on the `experiment results` directory within `projectFiles` — you'll see output files like:

- `experiment_results_[T*_*].part0`
- `experiment_results_[T*_*].part1`
- `experiment_results_[T*_*].part2`
- `experiment_results_[T*_*].part3`
- `experiment_results_[T*_*].txt`

where the first `*` in `T*_*` denotes the order of tournament selected in step 1, and the second `*` denotes the line number of the specific tournament from that same step.

The `.part` files are partial results, each written by one of your machine's processors working in parallel. On successful completion, these are compiled into the final `.txt` file with the same order-line designation.

The sample provided (order 3, line 2) took a moderately powered machine a little over 20 minutes to run to completion — your results may vary.

WARNING: the final `.txt` file will be approximately 4GB in size, if you are running multiple experiments 
one after the other, it is recommended that you either compress/move/delete result files as you go.

It is also recommended that you make liberal use of the CTRL+F function to navigate these result files in a timely fashion.
## authors/credits
- `oh-em-bee`, graduate of Vancouver Island University, researcher
- `Jacobus Swarts`, instructor at Vancouver Island University, research supervisor

Thank you to Vancouver Island University for funding this research project, and to the Math Department, and Cobus for 
giving me the opportunity to gain valuable experience in pursuing research. I'm sure the skills I'm gaining will carry 
through to all my future research projects. ~oh-em-bee

## future-work

## references
[1] Morgan Norge, Peter LaBarr, Isabella Brooke Sanders, and Dewey Taylor. **Kings in products of digraphs**. _Bull. Inst. Combin. Appl._, 100:111-122, 2024

## development-log
01/06/24 - repo setup, README - added `purpose`, `technologies-used`, `installation`, `authors/credits`, `references`, 
and `development-log` sections

BibTex Citation:
'''
@InProceedings{SciPyProceedings_11,
  author =       {Aric A. Hagberg and Daniel A. Schult and Pieter J. Swart},
  title =        {Exploring Network Structure, Dynamics, and Function using NetworkX},
  booktitle =   {Proceedings of the 7th Python in Science Conference},
  pages =     {11 - 15},
  address = {Pasadena, CA USA},
  year =      {2008},
  editor =    {Ga\"el Varoquaux and Travis Vaught and Jarrod Millman},
}
'''
