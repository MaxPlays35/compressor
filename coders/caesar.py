import typing
from coders import shannon


class CaesarEncryptor(shannon.ShannonEncoding):
    def __init__(self, file_in: typing.IO, file_out: typing.IO, progress_callback, key: int = 0):
        super().__init__(file_in, file_out, progress_callback)
        self._key = key

    def write_symbol(self, symbol: str):
        self.write_int((ord(symbol) + self._key), self._symbol_length)
    
    def write(self):
        super(CaesarEncryptor, self).write()


class CaesarDecryptor(shannon.ShannonDecoding):
    def __init__(self, file_in: typing.IO, file_out: typing.IO, progress_callback, key: int = 0):
        super().__init__(file_in, file_out, progress_callback)
        self._key = key

    def get_char(self, idx: int):
        idx -= self._key
        if idx < 0:
            idx += 255
        return super(CaesarDecryptor, self).get_char(idx)
    
    def read(self):
        super(CaesarDecryptor, self).read()

