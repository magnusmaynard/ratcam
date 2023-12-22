# RatCam :rat::movie_camera:
## Introduction
A simple method for tracking the paths of pesky rodents in my attic, so that the entry points can be blocked!

This is not a serious project, it was built for fun and a very specific need of mine. Feel free to repurpose it for other use-cases.

![Example output image](./docs/example_output.jpg)

## Packages
| Name                                        | Description                                                                              |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [:movie_camera: ratcam-capture](./capture/) | For acquiring videos of rats from the camera, to be run on the Jetson Nano.              |
| [:gear: ratcam-process](./process/)         | For analysing videos of rats, to be run on a desktop computer as a post-processing step. |
