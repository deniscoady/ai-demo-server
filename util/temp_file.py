from tempfile import NamedTemporaryFile

class TemporaryFile:
  def __init__(self, file, chunk_size = 4096, max_file_size = 256 * 1024 * 1024):
    self.file = file.file
    self.temp = NamedTemporaryFile(delete = True)
    self.chunk_size = chunk_size
    self.max_file_size = max_file_size
    pass
     
  async def __aenter__(self):
    for _ in range(0, int(self.max_file_size / self.chunk_size)): 
      chunk = self.file.read(self.chunk_size)
      if not chunk: break
      self.temp.write(chunk)
    return self.temp.name

  async def __aexit__(self, exception_type, exception_value, exception_traceback):
    self.temp.close()