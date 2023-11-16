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

    df_all_reviews, df_all_stats = extract_reproducibility_paragraph(paper_list, output_directory)

    df_all_reviews.to_csv(os.path.join(output_directory ,f'all_reviews.csv'), index = False, sep="\t", encoding='utf-8')
    df_all_stats.to_csv(os.path.join(output_directory ,f'all_stats.csv'), index = False, sep="\t", encoding='utf-8')

    # for category in list_categories_str:
    #     df_reviews = pd.read_csv(os.path.join(output_directory ,f'{category}_reviews2.csv'), sep= "\t", index_col=False)
    #     df_statistics = pd.read_csv(os.path.join(output_directory ,f'{category}_statistics.csv'), sep= "\t", index_col=False)

    #     df_all_reviews = pd.concat([df_all_reviews, df_reviews ])
    #     df_all_stats = pd.concat([df_all_stats, df_statistics ])
    
    df_all_stats = count_total_words(df_all_stats=df_all_stats, output_directory=output_directory)
    df_all_reviews.set_index(["id", "category"], inplace= True)
    df_all_reviews.sort_index(level = ['id', 'category'], ascending=True, inplace=True)

    histo_path = Path(output_directory) / "histo"
    if not histo_path.is_dir():
        os.mkdir(histo_path)
    save_hist(df_all_stats, histo_path)
    get_repro_copy_paste(df_all_reviews=df_all_reviews, output_directory=output_directory)

    resume(df_all_stats, output_directory=output_directory)


if __name__ == "__main__":
    cli()
