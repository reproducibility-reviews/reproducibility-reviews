# coding: utf8

import click
from pathlib import Path
import os
from extract_reviews_utils import (
    get_accepted_paper_list, 
    extract_reproducibility_paragraph,
    count_total_words,
    save_hist,
    get_repro_copy_paste,
    resume,
    count_checklist,
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
def cli(
    year, 
    output_directory,
):
    """
    Source code is available on GitHub: https://github.com/reproducibility-reviews/reproducibility-reviews .

    Do not hesitate to create an issue to report a bug or suggest an improvement.
    """
    paper_list = get_accepted_paper_list(year)

    if not output_directory.is_dir():
        os.mkdir(output_directory)

    path_all_reviews = Path(output_directory) / 'all_reviews.csv'
    path_all_stats = Path(output_directory) / 'all_stats.csv'

    if (not path_all_reviews.is_file()) or (not path_all_stats.is_file()):

        print(f"Extract reviews and count word for year {year}")
        df_all_reviews, df_all_stats = extract_reproducibility_paragraph(paper_list)

        df_all_reviews.to_csv(path_all_reviews, index = False, sep="\t", encoding='utf-8')
        df_all_stats.to_csv(path_all_stats, index = False, sep="\t", encoding='utf-8')

    else:

        print(f"Import tsv from {output_directory}")
        import pandas as pd
        df_all_reviews = pd.read_csv(path_all_reviews, sep= "\t", index_col=False)
        df_all_stats = pd.read_csv(path_all_stats, sep= "\t", index_col=False)

    
    print(f"Count total words")
    df_all_stats = count_total_words(df_all_stats=df_all_stats, output_directory=output_directory)
    df_all_reviews.set_index(["id", "category"], inplace= True)
    df_all_reviews.sort_index(level = ['id', 'category'], ascending=True, inplace=True)

    print(f"Creating histo")
    save_hist(df_all_stats, output_directory)

    print(f"Count number of copy/paste")
    get_repro_copy_paste(df_all_reviews=df_all_reviews, output_directory=output_directory)

    print(f"Create stats resume")
    resume(df_all_stats, output_directory=output_directory)

    print(f"Count checklist words in repro review")
    count_checklist(df_all_reviews=df_all_reviews, output_directory=output_directory, category="repro")


if __name__ == "__main__":
    cli()
