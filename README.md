# Reproducibility reviews

This repository aims to reproduce the results described in the following [paper](#Citation). 

These results correspond to an analysis of the reproducibility section of the reviews of the [MICCAI 2023 conference](https://conferences.miccai.org/2023/papers/).

The results were obtained as follows:
- [automatically extracting](#Extracting-the-reviews) the reviews of papers accepted at MICCAI
- [computing statistics regarding the reviews themselves](#Statistics-on-the-reviews) (e.g. word counts) (NOT on the human ratings of the reviews)
- [human rating](#Human-rating-of-the-reviews) of the reviews as described in the paper
- [analyzing inter-rater reliability](#Inter-rater-reliability)
- [analyzing the results of the human ratings](#Analyzing-the-ratings)
- [generating LaTeX](generate-latex) tables that were used in the paper or in the supplementary material 

## Citation

TODO: UPDATE CITATION

Colliot O, Thibeau-Sutre E, Brianceau C and Burgos N, Reproducibility in medical image computing *(In preparation)*

## Getting started

```
conda env create -f environment.yml
conda activate reproducibility-reviews
pip install -r requirements.txt
```

## Extracting the reviews

The reviews from MICCAI 2023 have already been extracted. If you wish, you may redo the extraction with the notebook `0. extract_reviews.ipynb`. This extracts the reviews of papers accepted at MICCAI conferences. By default, reviews from 2023 are extracted but you can change it to 2022. Note that we extract only the first 3 reviews for each paper to have a constant number of reviews in the analysis.

### Output files

The extraction outputs the following files in the `miccai_YYYY/extract-csv` directory:
- `reviews.csv`: complete reviews (all sections) for each paper + link to the code corresponding to the paper,
- `scores.csv`: scores given by reviewers for each paper,
- `count_words.csv`: number of words (for each section and total count) as computed from the `reviews.csv` file.
- `reproducibility_checklist_reviews.csv`: reviews ("reproducibility" section) that contain the word "checklist" or "check-list" or "check list"
- `reviews_copy_paste_10.csv`: reviews for which the "reproducibility" section contains copy/paste from other sections (need to have more than 10 consecutive words in common).

In addition, it will output an Excel file to be used for [human rating](Human-rating-of-the-reviews) in the `human_rating` directory:
- `reviews_reproducibility_YYYY.xlsx`: "reproducibility" section of the first 3 reviewers of all papers


## Statistics on the reviews

By running the notebook `1. reviews_stats.ipynb`, you can make some basic statistics regarding the reviews themselves (e.g. the number of words).

### Output files 

The notebook outputs 2 files in the `miccai_YYYY/stats` directory:
- `stats_word_count.csv`: file with statistics on the number of words.
- `data.json`: json file with some informations about the analysis (date, paths, number of papers, etc)

In addition, the notebook outputs histograms of word counts as png files in the `miccai_YYYY/histo` directory.

## Human rating of the reviews

Files related to human rating are within the `human_rating` directory.

As outlined in the paper, two raters evaluated the reviews of 90 papers (270 reviews). Their ratings are available in the files `rating_90/rating_90_{O,E}.csv`.

If you wish to perform your own ratings of the reviews. Please follow these steps:
- Take the extracted reviews which are available in `reviews_reproducibility_YYYY.xlsx`.
- Download the `template-rating.xlsx` file and paste the reviews into the dedicated columns.
- Rate the reviews and save the results in a CSV file.

## Inter-rater reliability

The notebook `2. inter_raters_analysis.ipynb` performs analysis of inter-rater reliability.

### Output files 

The notebook output the following 2 files `miccai_YYYY/stats_inter_raters` directory:
- `inter_raters_stats.csv`: file with the kappa cohen for the different rated items along with confidence intervals and standard errors.
- `data.json`: json file with some informations about analysis (date, paths, number of paper, etc)


## Analyzing the ratings

The notebook `3. rating_analysis.ipynb` performs the analysis of the reviews as assessed by human rating.

### Output files 

The notebook outputs the following files in the `miccai_YYYY/stats_rating` directory:
- various `.csv` containing the statistical analysis (proportions, kappa scores, confidence interval, etc)
- `data.json`: json file with some informations about the analysis (date, paths, number of paper, etc)

## Generate latex

The notebook `4. generate_latex.ipynb` reads the `.csv` files containing the results of the analysis and outputs a series of LaTeX files that were included in the paper or in the Supplementary Material.

### Output files 

After executing the notebook, you'll end with various  files in the `miccai_YYYY/latex` directory.
