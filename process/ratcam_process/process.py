import numpy as np
import cv2
from typing import Any, Union
from tqdm import tqdm
import os


def _process(
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


def process_video(
    video_path: str,
    interval_s: float,
    start_s: float,
    duration_s: Union[float, None],
    sensitivity: float,
    show: bool,
) -> bool:
    print("Processing video {video_path}")
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return False

    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    # Skip at interval
    if interval_s > 0:
        skip_count = int(interval_s * fps)
        print(f"Interval every {skip_count} frames")
    else:
        skip_count = 1

    # Skip to start
    if start_s > 0:
        frame_number = int(start_s * fps)
        print(f"Start from {start_s}s (#{frame_number})")
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)

    # Limit to duration
    if duration_s is not None:
        frame_number = int(duration_s * fps)
        print(f"Limiting to {frame_number} frames")
        total_frames = frame_number
    else:
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    current_frame = 0
    output_image = None
    subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

    with tqdm(total=total_frames) as pbar:
        while True:
            ret, frame = video.read()
            if not ret or current_frame > total_frames:
                break
            current_frame += 1
            pbar.update(1)

            if current_frame % skip_count != 0:
                continue

            output_image = _process(
                subtractor=subtractor,
                frame=frame,
                output_image=output_image,
                sensitivity=sensitivity,
            )

            if show:
                cv2.imshow("Preview", output_image)
                if cv2.waitKey(1) == ord("q"):
                    break

    if output_image is not None:
        output_path = "output.png"
        print(f"Saving image: {output_path}")
        cv2.imwrite(output_path, output_image)

    video.release()
    cv2.destroyAllWindows()

    return True
