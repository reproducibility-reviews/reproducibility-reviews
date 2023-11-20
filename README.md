# Reproducibility reviews

This repository aims to reproduce the results described in the following paper on "Reproducibility in medical image computing". 

These results correspond to an analysis of the reproducibility section of the reviews of the [MICCAI 2023 conference](https://conferences.miccai.org/2023/papers/).

The results were obtained as follows:
1. automatically extracting the reviews of papers accepted at MICCAI (using the [command-line tool](#Extracting-the-reviews))
2. human rating of the reviews as described in the paper
3. analyzing the ratings of these reviews (presented as a [Jupyter notebook](#Analyzing-the-ratings))

## Citation

Colliot O, Thibeau-Sutre E, Brianceau C and Burgos N, Reproducibility in medical image computing *(In preparation)*

## Getting started

```
conda env create -f environment.yml
conda activate reproducibility-reviews
pip install -r requirements.txt
```

## Extracting the reviews

This task can be run with the following command line:
```Text
python ./src/cli.py extract-reviews [OPTIONS]
```
where:

- `year`: (str) the year of the MICCAI conference for which you want to extract the reviews (currently only supports 2022 or 2023, default is 2023).
- `output_directory`: (Path) the path to the directory where you want to save your results (default is results).


## Analyzing the ratings

## External ressources

## Citing us

