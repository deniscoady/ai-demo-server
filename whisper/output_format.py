import json
from webvtt import WebVTT, Caption
from datetime import timedelta

class OutputFormat:
  def __call__(self, segments):
    return json.dumps(segments)
  

class WebvttOutputFormat(OutputFormat):
  def strftime(self, seconds: float):
    td = timedelta(seconds = seconds)

    milliseconds     = td.microseconds // 1000
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    hours        = int(hours)
    minutes      = int(minutes)
    seconds      = int(seconds)
    milliseconds = int(milliseconds)
    # Format it as HH:MM:SS.mmm (3-digit milliseconds)
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    return formatted_time
  
  def __call__(self, segments):
    vtt = WebVTT()
    for segment in segments:
      start = self.strftime(segment.start)
      end   = self.strftime(segment.end)
      text  = segment.text
      vtt.captions.append(Caption(start, end, text))
    return vtt.content
