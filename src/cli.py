# coding: utf8

import click
from pathlib import Path
from extract_reviews import cli as extract_reviews_cli
from random_reviews import cli as random_reviews_cli

CONTEXT_SETTINGS = dict(
    # Extend content width to avoid shortening of pipeline help.
    max_content_width=160,
    # Display help string with -h, in addition to --help.
    help_option_names=["-h", "--help"],
)



@click.group(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.version_option()

def cli():

    print()

cli.add_command(extract_reviews_cli)
cli.add_command(random_reviews_cli)


if __name__ == "__main__":
    cli()
