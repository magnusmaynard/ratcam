# RatCam :rat::camera:
Simple programs for tracking the paths of pesky rodents in my attic, so that the entry points can be blocked.

This projects is divided into two seperate poetry packages:
- [ratcam-capture](./capture/) - For aquiring videos from the camera, to be run on the Jetson Nano
- [ratcam-process](./process/) - For analysing these video for rats, to be run on a desktop computer as a post-processing step.
