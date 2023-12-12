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

There are two ways to extract the reviews of papers accepted at MICCAI conferences:

### with the command-line tool
This task can be run with the following command line:
```Text
python ./src/cli.py extract-reviews [OPTIONS]
```
where [OPTIONS] can be:

- `--year, -y`: (str) the year of the MICCAI conference for which you want to extract the reviews (currently only supports 2022 or 2023, default is 2023).
- `--output_directory, -od`: (Path) the path to the directory where you want to save your results (default is results). 
- `--extract_copy_paste`: (bool) to extract the list of reproducibility reviews for which the content is a copy/paste of another category review.
- `--extract_checklist`: (bool) to extract the list of reproducibility reviews for which the content contain the word "checklist".
 
### with the notebook 
You can also use the note book `extract_reviews.ipynb` to extract the reviews if you are not comfortable with the commandline.

### Output files

With both methods, you'll end with at least 3 files in the `miccai_202X` directory:
- `reviews.csv`: file with all the reviews of 3 different reviewers for each paper,
- `scores.csv`: file with all the scores of 3 different reviewers for each paper,
- `count_words.csv`: file with the number of words for all the reviews in the `reviews.csv` file.

and a file in the `rating` directory:
- `reviews_repro_202X.xlsx`: file with the reproduciblity review from 3 different reviewers for each paper and the link to a git repository when provided. 


## Human rating of the reviews

As outlined in the paper, two raters evaluated the initial 90 reviews to conduct an inter-rater analysis. Subsequently, another rater assessed the reviews of all papers accepted at MICCAI 2023.

If desired, you have the option to use your own ratings for the reviews. To do so, please follow these steps:

- Extract the reviews of the papers accepted at MICCAI (specify the year), in the `reviews_repro_202X.xlsx`.
- Download the `template-rating.xlsx` file and paste the reviews into the designated blank spaces.
- Evaluate the reviews and save the results in a CSV file.
- Analyze the results as explained in the next section.

## Analyzing the ratings

### Inter-rater analysis

### Rating analysis

## External ressources



