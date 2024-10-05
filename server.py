from aiohttp import web
from datetime import datetime
import torch
from util.temp_file import TemporaryFile
from whisper.transcription import TranscriptionService



class OpenAICompatibleServer:

    def __init__(self, host = '0.0.0.0', port = 8000):
      self.host = host
      self.port = port
      self.lock = False
      self.file = None
      self.time = datetime.now()
      device  = 'cuda' if torch.cuda.is_available() else 'cpu'
      self.whisper = TranscriptionService('distil-large-v3', device = device)

    async def transcribe(self, request):
      if self.lock: web.Response(status = 429)
      self.lock = True
      self.file = data['file'].filename

      data = await request.post()
      file = data['file']
      json = {}

      async with TemporaryFile(file) as filename:
        json['text'] = self.whisper.transcribe(filename, 'vtt')
        self.lock = False
        return web.json_response(json)

      self.file = None      
      self.lock = False
      return web.Response(status = 500)

    async def overview(self, request):
      return web.json_response({
        'lock': self.lock,
        'file': self.file,
        'time': str(self.time)
      })

    def run(self):
      app = web.Application(client_max_size = 256 * 1024 * 1024)
      app.router.add_get ('/', self.overview)
      app.router.add_post('/v1/audio/transcriptions', self.transcribe)
      web.run_app(app, host = self.host, port = self.port)

# Run the web server
if __name__ == '__main__':
  server = OpenAICompatibleServer()
  server.run()
