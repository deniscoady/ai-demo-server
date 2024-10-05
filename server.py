from aiohttp import web
from datetime import datetime, timedelta
import torch
from util.temp_file import TemporaryFile
from whisper.transcription import TranscriptionService
import uvicorn


class WhisperServer:

    def __init__(self, host = '0.0.0.0', port = 8000):
      self.host = host
      self.port = port
      self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
      print(f'WhisperServer:')
      print(f'  device = {self.device}')

    async def transcribe(self, request):
      data  = await request.post()
      file  = data['file']
      model = data['model']
      model = model if model != 'whisper-1' else 'distil-large-v3'

      print('')
      print(f'{str(datetime.now())}')
      print(f'  filename = {file.filename}')
      print(f'  model    = {model}')

      async with TemporaryFile(file) as filename:
        whisper = TranscriptionService(model, device = self.device)
        text    = whisper.transcribe(filename, 'vtt')
        return web.json_response({'text' : text })

    def run(self):
      app = web.Application(client_max_size = 256 * 1024 * 1024)
      app.router.add_post('/v1/audio/transcriptions', self.transcribe)
      web.run_app(app, host = self.host, port = self.port)



# Run the web server
if __name__ == '__main__':
  server = WhisperServer()
  server.run()
