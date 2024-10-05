from aiohttp import web
from datetime import datetime, timedelta
import torch
from util.temp_file import TemporaryFile
from whisper.transcription import TranscriptionService
import uvicorn


class WhisperServer:

    def __init__(self):
      self.lock = False
      self.file = None
      self.time = None
      self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    async def transcribe(self, request):
      if self.lock: web.Response(status = 429)
      self.lock = True
      data = await request.post()
      file = data['file']
      model = data['model']
      model = model if model != 'whisper-1' else 'distil-large-v3'
      self.file = file.filename
      self.time = datetime.now()

      async with TemporaryFile(file) as filename:
        whisper = TranscriptionService(model, device = self.device)
        text    = whisper.transcribe(filename, 'vtt')
        self.lock = False
        return web.json_response({'text' : text })

      self.file = None      
      self.lock = False
      return web.Response(status = 500)

    async def overview(self, request):
      now = datetime.now() 
      duration = timedelta(seconds = 0) if self.time == None else now - self.time
      return web.json_response({
        'lock': self.lock,
        'file': self.file,
        'time': str(duration)
      })

    def app(self):
      app = web.Application(client_max_size = 256 * 1024 * 1024)
      app.router.add_get ('/', self.overview)
      app.router.add_post('/v1/audio/transcriptions', self.transcribe)
      return app


server = WhisperServer()
app = server.app()

# Run the web server
if __name__ == '__main__':
  web.run_app(app, host = '0.0.0.0', port = 8000)
