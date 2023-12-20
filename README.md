# Reproducibility reviews

This repository aims to reproduce the results described in the following paper on "Reproducibility in medical image computing". 

These results correspond to an analysis of the reproducibility section of the reviews of the [MICCAI 2023 conference](https://conferences.miccai.org/2023/papers/).

The results were obtained as follows:
1. automatically extracting the reviews of papers accepted at MICCAI (presented as a [Jupyter notebook](#Analyzing-the-ratings))
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

You need to run the notebook `0. extract_reviews.ipynb` to extract the reviews of papers accepted at MICCAI conferences.

### Output files

After executing the notebook, you'll end with 6 in the `miccai_YYYY/extract-csv` directory:
- `reviews.csv`: file with all the reviews of 3 different reviewers for each paper,
- `scores.csv`: file with all the scores of 3 different reviewers for each paper,
- `count_words.csv`: file with the number of words for all the reviews in the `reviews.csv` file.
- `reproducibility_checklist_reviews.csv`: file with the reproducibility reviews that contain the word "checklist" or "check-list" or "check list"
- `reviews_copy_paste_10.csv`: file with reviews which contain copy/paste from other parts (need to have more than 10 consecutive words in common).
- `reviews_wo_copy_paste_10.csv`: file without reviews which contain copy/paste from other parts.


## Automatic analysis of the reviews

By running the notebook `1. reviews_stats.ipynb`, you can make some basic statistics regarding the number of words, create histograms and calculate some correlation factors.

### Output files 

After executing the notebook, you'll end with 2 files in the `miccai_YYYY/stats` directory:
- `stats_word_count.csv`: file with statistics on the number of words.
- `data.json`: json file with some informations about your experiment (date, paths, number of paper, etc)


## Human rating of the reviews

As outlined in the paper, two raters evaluated the initial 90 reviews to conduct an inter-rater analysis. Subsequently, another rater assessed the reviews of all papers accepted at MICCAI 2023.

If desired, you have the option to use your own ratings for the reviews. To do so, please follow these steps:

- Extract the reviews of the papers accepted at MICCAI (specify the year), in the `reviews_repro_202X.xlsx`.
- Download the `template-rating.xlsx` file and paste the reviews into the designated blank spaces.
- Evaluate the reviews and save the results in a CSV file.

## Inter raters analysis

By running the notebook `2. inter_raters_analysis.ipynb`, you can compare two different ratings.

### Output files 

After executing the notebook, you'll end with 2 files in the `miccai_YYYY/stats_inter_raters` directory:
- `inter_raters_stats.csv`: file with the kappa cohen factor with its confidence intervals and standard errors.
- `data.json`: json file with some informations about your experiment (date, paths, number of paper, etc)


## Analyzing the ratings

By running the notebook `3. rating_analysis.ipynb`, you can make some basic statistics regarding the number of words, create histograms and calculate some correlation factors.

### Output files 

After executing the notebook, you'll end with 2 files in the `miccai_YYYY/stats_rating` directory:
- `1-category.csv`: file with statistics on the number of words.
- `2.
- `data.json`: json file with some informations about your experiment (date, paths, number of paper, etc)

## Generate latex

By running the notebook `4. generate_latex.ipynb`, you.

### Output files 

After executing the notebook, you'll end with 2 files in the `miccai_YYYY/latex` directory:
- `1-category.csv`: file with statistics on the number of words.
- `2.
- `data.json`: json file with some informations about your experiment (date, paths, number of paper, etc)

## External ressources



