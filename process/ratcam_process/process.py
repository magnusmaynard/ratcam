from unicodedata import name
import numpy as np
import cv2
from typing import Any, Union
from tqdm import tqdm
import os


def _process_image(
    subtractor: Any,
    frame: np.ndarray,
    output_image: Union[np.ndarray, None],
    sensitivity: float,
) -> np.ndarray:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = subtractor.apply(frame)

    if output_image is None:
        output_image = np.zeros_like(frame)

    return cv2.addWeighted(
        src1=output_image, src2=mask, alpha=1.0, beta=sensitivity, gamma=0
    )


def _process_video(
    video_path: str,
    interval_s: float,
    sensitivity: float,
    preview: bool,
    output_image: Union[np.ndarray, None],
) -> Union[np.ndarray, None]:
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    if interval_s > 0:
        # Skip at interval
        skip_count = int(interval_s * fps)
        print(f"Processing every {skip_count} frames [Interval={interval_s}s, FPS={fps}]")
    else:
        # Every frame
        skip_count = 1

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

    with tqdm(total=total_frames) as pbar:
        pbar.set_description("Frames in video")
        while True:
            ret, frame = video.read()
            if not ret or current_frame > total_frames:
                break
            current_frame += 1
            pbar.update(1)

            if current_frame % skip_count != 0:
                continue

            output_image = _process_image(
                subtractor=subtractor,
                frame=frame,
                output_image=output_image,
                sensitivity=sensitivity,
            )

            if preview:
                cv2.imshow("Preview", output_image)
                if cv2.waitKey(1) == ord("q"):
                    break

    video.release()
    cv2.destroyAllWindows()

    return output_image

def process(
    dir_path: str,
    interval_s: float,
    sensitivity: float,
    preview: bool,
    extension: str,
    output_path: str):

    if  not os.path.isdir(dir_path):
        print(f"Invalid directory: {dir_path}")
        return False

    print(f"Processing directory: {dir_path}")

    video_paths = [os.path.join(dir_path, filename) for filename in sorted(os.listdir(dir_path)) if filename.endswith(extension)]
    output_image = None

    with tqdm(total=len(video_paths)) as pbar:
        pbar.set_description("Videos")
        for video_path in video_paths:
            output_image = _process_video(video_path=video_path, interval_s=interval_s,sensitivity=sensitivity, preview=preview, output_image=output_image)

            if output_image is None:
                print(f"Failed to process video: {video_path}")
                return False

            cv2.imwrite(output_path, output_image)
            pbar.update(1)

    print(f"Processing complete, final image saved to: {output_path}")
    return True
