# Reproducibility reviews repo

This Git repository aims to reproduce the results described in the chapter on reproducibility in neuroimaging and deep learning for the MICCAI book.
The repository is organized into two parts. The first part is dedicated to retrieving and analyzing the reviews of papers accepted at MICCAI. 
The second part, presented as a Jupyter notebook, focuses on analyzing the ratings of these reviews.

## Getting started

```bash
$ conda env create -f environment.yml
$ conda activate reproducibility-reviews
$ pip install -r requirements.txt
```

## Running the task

This task can be run with the following command line:
```Text
python ./src/cli.py extract-reviews [OPTIONS]
```
where:

- `year`: (str) the year of the MICCAI conference for which you want to extract the reviews (currently only supports 2022 or 2023, default is 2023).
- `output_directory`: (Path) the path to the directory where you want to save your results (default is results).


## Launch the jupyter-notebook 

## External ressources

## Citing us

