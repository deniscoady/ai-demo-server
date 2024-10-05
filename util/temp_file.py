from tempfile import NamedTemporaryFile
import magic

class TemporaryFile:
  def __init__(self, file, chunk_size = 4096, max_file_size = 256 * 1024 * 1024):
    self.file = file
    mime = magic.Magic(mime = True)
    mime_type = mime.from_buffer(file.peek(2048))
    extension = self.get_file_extension(file)
    print(f'mime type = {mime_type}')
    self.temp = NamedTemporaryFile(delete = True, suffix = '.' + 'wav')
    self.chunk_size = chunk_size
    self.max_file_size = max_file_size
    pass
     
  def get_file_extension(self, file):
    mime = magic.Magic(mime = True)
    mime_type = mime.from_buffer(file.peek(2048))
    match mime_type:
      case 'audio/ogg'  : return 'ogg'
      case 'audio/mp4'  : return 'mp4'
      case 'audio/mp3'  : return 'mp3'
      case 'audio/wav'  : return 'wav'
      case 'audio/x-wav': return 'wav'
      case _            : return mime_type.split('/')[1]

  async def __aenter__(self):
    for _ in range(0, int(self.max_file_size / self.chunk_size)): 
      chunk = self.file.read(self.chunk_size)
      if not chunk: break
      self.temp.write(chunk)
    return self.temp.name

  async def __aexit__(self, exception_type, exception_value, exception_traceback):
    self.temp.close()