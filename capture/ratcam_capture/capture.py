import gi
import sys
import os
import datetime

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True


def capture(output_dir: str) -> None:
  GObject.threads_init()
  Gst.init(None)

  fps = 2
  output_dir = os.path.join(output_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
  flip_method = 2 # 180 deg
  timesplit_24h = 8.64e+13
  timesplit_1h = 3.6e+12
  timesplit_10min = 6e+11
  timesplit_10s = 1e+10

  os.makedirs(output_dir, exist_ok=True)

  pipeline_str = f"\
    nvarguscamerasrc sensor_id=0 ! video/x-raw(memory:NVMM),width=4608,height=2592,framerate=14/1, format=NV12 ! \
    nvvidconv flip-method={flip_method} ! video/x-raw,width=2304,height=1296 ! \
    videorate ! video/x-raw,width=2304,height=1296,framerate={fps}/1 ! \
    clockoverlay halignment=right valignment=bottom shaded-background=true time-format='%D %H:%M:%S' ! \
    x264enc ! splitmuxsink location={output_dir}/video%02d.mp4 max-size-time={int(timesplit_10s)}"

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
