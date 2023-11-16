# coding: utf8

import click
from pathlib import Path
from get_reviews import get_accepted_paper_list, extract


@click.command(name="random-reviews", no_args_is_help=True)
@click.option(
    "--year",
    "-y",
    help = "Choose the year of the MICCAI conference for which you want to extract reviews of accepted papers.",
    default = "2023",
    type = click.Choice(["2022", "2023"]),
    )
@click.option(
    "--input_file",
    "-if",
    help = "file with the extracted reviews",
    default = "results",
    type = click.Path(path_type=Path),
    )
def cli(
    year, 
    input_file,
):
    import pandas as pd
    df = pd.read_csv(input_file,  sep= "\t", index_col=False)

    ## TO FINISH 
    # nb_reviews = 
    # print("*" * 100)
    # print(f"{nb_reviews} random reviews between {lower_bound*10} and {upper_bound*10} percentiles")
    # print("*" * 100)
    
    # lower_bound_40th = deciles[lower_bound]
    # upper_bound_60th = deciles[upper_bound]

    # selected_reviews = reviews[
    #     ((data_frame['Review 1'] >= lower_bound_40th) & (data_frame['Review 1'] <= upper_bound_60th)) |
    #     ((data_frame['Review 2'] >= lower_bound_40th) & (data_frame['Review 2'] <= upper_bound_60th)) |
    #     ((data_frame['Review 3'] >= lower_bound_40th) & (data_frame['Review 3'] <= upper_bound_60th))
    # ]

    # selected_reviews_sample = selected_reviews.sample(nb_reviews)

    # for _, row in selected_reviews_sample.iterrows():
    #     for col in ["Review 1", "Review 2", "Review 3"]:
    #         x = df.at[_, col]
    #         if ((x >= lower_bound_40th) & (x<= upper_bound_60th)):
    #             #print(f"{col}:")
    #             print(row[col])
    #             print(f"Word Count: {x}")
    #             print("-" * 50)




if __name__ == "__main__":
    cli()
