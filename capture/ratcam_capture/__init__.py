import click
from ratcam_capture.capture import capture
from typing import Union
import os

@click.command(help="Capture a video from RPI an camera and save to disk")
@click.option("--output-directory", "-o", required=True, type=str, help="Path to output directory where videos are saved")
@click.option("--split", "-s", type=int, help="Seconds between each video split",
    show_default=True, default=600)
@click.option("--flip", type=int, help="Flip orientation of output video. 0=none, 1=CCW, 2=180, 3=CW", show_default=True, default=2)
@click.option("--fps", type=int, help="FPS of output video, max is 14.", show_default=True, default=4)
def main(output_directory: str, split: int, flip: int, fps: int) -> bool:
    if capture(output_dir=output_directory, split_s=split, flip_mode=flip, fps=fps):
        exit(os.EX_OK)
    else:
        exit(os.EX_IOERR)
