import gi
import sys
import os
import datetime

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def bus_call(bus, message, loop):
    if message.type == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()
    elif message.type == Gst.MessageType.ERROR:
        error, debug = message.parse_error()
        print(f"Error: {error}: {debug}", file=sys.stderr)
        loop.quit()
    return True


def capture(output_dir: str, split_s: int, flip_mode: int, fps: int) -> None:
  GObject.threads_init()
  Gst.init(None)

  output_dir = os.path.join(output_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
  os.makedirs(output_dir, exist_ok=True)

  pipeline_str = f"\
    nvarguscamerasrc sensor_id=0 ! video/x-raw(memory:NVMM),width=4608,height=2592,framerate=14/1, format=NV12 ! \
    nvvidconv flip-method={flip_mode} ! video/x-raw,width=2304,height=1296 ! \
    videorate ! video/x-raw,width=2304,height=1296,framerate={fps}/1 ! \
    clockoverlay halignment=right valignment=bottom shaded-background=true time-format='%D %H:%M:%S' ! \
    x264enc ! \
    splitmuxsink location={output_dir}/video%04d.mp4 max-size-time={int(split_s*1e+9)} async-handling=1 send-keyframe-requests=1"

  pipeline = Gst.parse_launch(pipeline_str)
  bus = pipeline.get_bus()

  loop = GObject.MainLoop()
  bus.add_signal_watch()
  bus.connect ("message", bus_call, loop)

  pipeline.set_state(Gst.State.PLAYING)
  try:
    loop.run()
  except:
    pass

  pipeline.set_state(Gst.State.NULL)
