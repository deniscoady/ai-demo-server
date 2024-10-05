from faster_whisper import WhisperModel
from .output_format import OutputFormat, WebvttOutputFormat


class TranscriptionService:
  def __init__(self, model_name, device = "cuda", beam_size = 5):
    self.beam_size = beam_size
    self.model     = WhisperModel(model_name, 
      device       = device, 
      compute_type = 'float16' if device == 'cuda' else 'int8')
    

  def transcribe(self, audio_filename, output_format = 'json'):
    formatter = OutputFormat() 
    if output_format in ['vtt', 'webvtt']: formatter = WebvttOutputFormat()

    segments, info = self.model.transcribe(audio_filename, beam_size = self.beam_size)
    segments = list(segments)
    result   = formatter(segments)
    return result