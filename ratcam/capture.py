
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import os
import time

# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

def _get_video_path(directory: str, index: int) -> str:
    return os.path.join(directory, f"capture_{index}.h264")


def capture_video(directory: str, split_s: int) -> bool:

#     with picamera.PiCamera(resolution=(4608, 2592)) as camera:
#         index = 0
#         camera.start_recording(_get_video_path(directory, index))
#         try:
#             while True:
#                 camera.split_recording(_get_video_path(directory, index))
#                 camera.wait_recording(split_s)
#         finally:
#             camera.stop_recording()
#     return True


    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration())
    encoder = H264Encoder()
    picam2.start_recording(encoder, _get_video_path(directory, index), quality=Quality.HIGH)
    time.sleep(10)
    picam2.stop_recording()
