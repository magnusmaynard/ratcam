import click
from ratcam.process import process_video
from ratcam.capture import capture_video
from typing import Union
import os


@click.group()
def cli():
    """A simple program for tracking the paths of pesky rodents in my attic, so that the entry points can be blocked."""
    pass


@click.command(help="Capture a video from RPI an camera and save to disk")
@click.option("--output-directory", "-o", required=True, type=str, help="Path to output directory where videos are saved")
@click.option(
    "--split",
    "-v",
    required=False,
    type=int,
    show_default=True,
    default=86400,
    help="Seconds between each video file split, default is a new file every 24h.",
)
def capture(output_directory: str, split: int) -> bool:
    if capture_video(directory=output_directory, split_s=split):
        exit(os.EX_OK)
    else:
        exit(os.EX_IOERR)


@click.command(help="Process a capture video file")
@click.option("--video-path", "-v", required=True, type=str, help="Path to video file")
@click.option(
    "--interval",
    "-i",
    required=False,
    type=float,
    show_default=True,
    default=1.0,
    help="Interval in seconds between every processed frames",
)
@click.option(
    "--start",
    "-s",
    required=False,
    type=float,
    show_default=True,
    default=0,
    help="Time in seconds to processing from",
)
@click.option(
    "--duration",
    "-d",
    required=False,
    type=float,
    show_default=True,
    default=None,
    help="Time in seconds to process for",
)
@click.option(
    "--sensitivity",
    "-f",
    required=False,
    type=float,
    show_default=True,
    default=0.01,
    help="The amount the background changes are added to output image",
)
@click.option(
    "--show",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Show preview of processed frames",
)
def process(
    video_path: str,
    interval: float,
    start: float,
    duration: Union[float, None],
    sensitivity: float,
    show: bool,
) -> bool:
    if process_video(
        video_path=video_path,
        interval_s=interval,
        start_s=start,
        duration_s=duration,
        sensitivity=sensitivity,
        show=show,
    ):
        exit(os.EX_OK)
    else:
        exit(os.EX_IOERR)


cli.add_command(capture)
cli.add_command(process)
