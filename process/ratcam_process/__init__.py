import click
from ratcam_process.process import process
from typing import Union
import os


@click.command(help="Process a captured video file")
@click.option(
    "--directory",
    "-d",
    required=True,
    type=str,
    help="Path to directory containing .mp4 video files",
)
@click.option(
    "--interval",
    "-i",
    required=False,
    type=float,
    show_default=True,
    default=0.0,
    help="Interval in seconds between every processed frames, 0 processes every frame",
)
@click.option(
    "--sensitivity",
    "-s",
    required=False,
    type=float,
    show_default=True,
    default=0.01,
    help="The amount background changes affect the final output image",
)
@click.option(
    "--show-preview",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Show preview of processed frames",
)
@click.option(
    "--output",
    "-o",
    required=False,
    type=str,
    show_default=True,
    default="output.jpg",
    help="Path to save resulting output image",
)
def main(
    directory: str,
    interval: float,
    sensitivity: float,
    show_preview: bool,
    output: str,
) -> bool:
    if process(
        dir_path=directory,
        interval_s=interval,
        sensitivity=sensitivity,
        preview=show_preview,
        output_path=output,
    ):
        exit(os.EX_OK)
    else:
        exit(os.EX_IOERR)
