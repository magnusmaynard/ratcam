# RatCam
A simple program for tracking the paths of pesky rodents in my attic, so that the entry points can be blocked.

Hardware used:
- Jetson Nano
- Raspberry Pi NoIR Camera v3
- IR illuminator to light the space

The footage is saved to a memory card, which can later be post-processed to generate a heatmap of the paths.

## Link
https://docs.opencv.org/3.4/d2/d55/group__bgsegm.html
https://docs.opencv.org/3.4/d6/d17/group__cudabgsegm.html
https://github.com/robertosannazzaro/motion-heatmap-opencv/blob/master/motion_heatmap.py

gstreamer to use nvdec:
```
time GST_DEBUG=3 gst-launch-1.0 filesrc location=/data/traffic.m4v ! qtdemux !  h264parse ! nvdec ! fakesink sync=false
```
gstreamer decode to skip frames:


## Setup


## Run
poetry run ratcam process -v "/home/magnus/github/ratcam/data/traffic.m4v"

gst-launch-1.0 filesrc location=/data/traffic.m4v ! qtdemux ! decodebin ! videoconvert ! videoscale ! autovideosink


## deps
sudo apt install libcap-dev
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip
