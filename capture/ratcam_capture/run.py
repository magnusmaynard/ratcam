import click
from ratcam_capture.capture import capture_video
from typing import Union
import os

@click.command(help="Capture a video from RPI an camera and save to disk")
@click.option("--output-directory", "-o", required=True, type=str, help="Path to output directory where videos are saved")
def capture(output_directory: str) -> bool:
    if capture_video(output_dir=output_directory):
        exit(os.EX_OK)
    else:
        exit(os.EX_IOERR)
