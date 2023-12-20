# Rat Cam - Process
This could be done on the Nano, but it is recommended to run on seperate desktop machine for performance reasons. This is done after images have been aquired as a post processing step.

## Setup
1. Clone this repo.
2. Install and build poetry package:
    ```
    cd ratcam/capture
    poetry install
    poetry build
    pip3 install --editable .
    ```
## Run
poetry run ratcam process -v "/home/magnus/github/ratcam/data/traffic.m4v"

gst-launch-1.0 filesrc location=/data/traffic.m4v ! qtdemux ! decodebin ! videoconvert ! videoscale ! autovideosink


## deps
poety
sudo apt install libcap-dev
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip


## Links
https://docs.opencv.org/3.4/d2/d55/group__bgsegm.html
https://docs.opencv.org/3.4/d6/d17/group__cudabgsegm.html
https://github.com/robertosannazzaro/motion-heatmap-opencv/blob/master/motion_heatmap.py

gstreamer to use nvdec:
```
time GST_DEBUG=3 gst-launch-1.0 filesrc location=/data/traffic.m4v ! qtdemux !  h264parse ! nvdec ! fakesink sync=false
```
gstreamer decode to skip frames:


gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! 'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=2 ! 'video/x-raw, width=816, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e
