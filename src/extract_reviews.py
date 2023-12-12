# coding: utf8

import click
from pathlib import Path
import os
from extract_reviews_utils import (
    get_accepted_paper_list, 
    extract_paragraph,
    count_total_words,
    get_repro_copy_paste,
    count_checklist,
    create_rating_excel,
)

@click.command(name="extract-reviews", no_args_is_help=True)
@click.option(
    "--year",
    "-y",
    help = "Choose the year of the MICCAI conference for which you want to extract reviews of accepted papers.",
    default = "2023",
    type = click.Choice(["2022", "2023"]),
    )
@click.option(
    "--output_directory",
    "-od",
    help = "Directory where the output TSV and images will be saved.",
    default = "results",
    type = click.Path(path_type=Path),
    )
@click.option(
    "--extract_copy_paste",
    "-ecp",
    help = "to extract the list of reproducibility reviews for which the content is a copy/paste of another category review.",
    default = False,
    type = bool,
    is_flag = True,
    )
@click.option(
    "--extract_checklist",
    "-od",
    help = "to extract the list of reproducibility reviews for which the content contain the word 'checklist'.",
    default = False,
    type = bool,
    is_flag = True,
    )
def cli(
    year, 
    output_directory,
    extract_copy_paste,
    extract_checklist,
):
    """
    Source code is available on GitHub: https://github.com/reproducibility-reviews/reproducibility-reviews .

    Do not hesitate to create an issue to report a bug or suggest an improvement.
    """
    paper_list = get_accepted_paper_list(year)

    # create th output directory 
    output_directory = Path(f"miccai{year}")
    if not output_directory.is_dir():
        os.mkdir(output_directory)
    path_all_reviews = output_directory / 'reviews.csv'
    path_all_stats = output_directory / 'count_words.csv'
    path_all_scores = output_directory / 'scores.csv'

   # extract 7 min  
    if (not path_all_reviews.is_file()) or (not path_all_stats.is_file()):

        print(f"Extract reviews and count word for year {year}")
        df_all_reviews, df_all_stats, df_all_scores = extract_paragraph(paper_list, year)


        df_all_scores.to_csv(path_all_scores, index = True, sep="\t", encoding='utf-8')
        df_all_reviews.to_csv(path_all_reviews, index = True, sep="\t", encoding='utf-8')
        df_all_stats.to_csv(path_all_stats, index = True, sep="\t", encoding='utf-8')

    else:
        import pandas as pd
        print(f"Import tsv from {output_directory}")

        df_all_reviews = pd.read_csv(path_all_reviews, sep= "\t",  header=[0, 1], index_col=[0,1], skip_blank_lines=True)
        df_all_stats = pd.read_csv(path_all_stats, sep= "\t",  header=[0, 1], index_col=[0,1], skip_blank_lines=True)


    print(f"Count total words")
    df_all_stats = count_total_words(df_all_stats=df_all_stats, output_directory=output_directory)

    if extract_copy_paste:
        print(f"Count number of copy/paste")
        get_repro_copy_paste(df_all_reviews=df_all_reviews, output_directory=output_directory)

    if extract_checklist:
        print(f"Count checklist words in repro review")
        count_checklist(df_all_reviews=df_all_reviews, output_directory=output_directory, category="reproducibility")

    print("Create rating excel file")
    create_rating_excel(df_all_reviews= df_all_reviews, year_=year, output_directory= output_directory)
    
if __name__ == "__main__":
    cli()
