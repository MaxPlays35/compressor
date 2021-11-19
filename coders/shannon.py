import collections
import typing
from math import ceil, log2, modf, copysign, fabs, floor


def get_bx_list(probabilities: list[tuple[str, float]]):
    bx = [(probabilities[0][0], "0.0000000000000000000000000000000000000")]
    prev = probabilities[0][1]
    for letter, value in probabilities[1:]:
        bx.append((letter, prev))
        prev += value

    return bx


def double_to_binary(double: float) -> str:
    bits = abs(ceil(log2(double)))
    sign = '-' * (copysign(1.0, double) < 0)
    frac, fint = modf(fabs(double))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    # print(f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}')
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'


class ShannonEncoding:
    def __init__(self, file_in: typing.IO, file_out: typing.IO, progress_callback) -> None:
        self._file_in = file_in
        self._file_out = file_out
        self._text = file_in.read()
        self._progress_callback = progress_callback
        self._symbol_length = 0

    def get_alphabet(self):
        counted_letters = collections.Counter(self._text)
        lenght = len(self._text)
        probabilities = {}
        for (key, value) in counted_letters.most_common():
            probabilities.update({
                key: value / lenght
            })
        probabilities = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
        encoded_letters = []
        # [('e', 0.35), ('b', 0.2), ('f', 0.15), ('a', 0.1), ('c', 0.1), ('d', 0.1)]
        for idx, item in enumerate(get_bx_list(probabilities)):
            if isinstance(item[1], float):
                encoded_letters.append(
                    (item[0], double_to_binary(item[1])[2:ceil(abs(log2(probabilities[idx][1]))) + 2]))
            else:
                encoded_letters.append((item[0], item[1][2:ceil(abs(log2(probabilities[idx][1]))) + 2]))
        return dict(encoded_letters)

    def write_int(self, integer: int, length: int):
        self._file_out.write(integer.to_bytes(length, 'little'))

    def write_symbol(self, symbol: str):
        self.write_int(ord(symbol), self._symbol_length)

    def next_section(self, symbol_length=1):
        self._file_out.write((chr(0) * symbol_length).encode("utf-8"))

    def code_separator(self):
        self._file_out.write(chr(1).encode("utf-8"))

    def write(self):
        alphabet = self.get_alphabet()
        encoded_data = ''
        for char in self._text:
            encoded_data += alphabet[char]

        length = len(encoded_data)
        self.write_int(length, 4)
        self._symbol_length = ceil(log2(ord(max(alphabet.keys(), key=lambda x: ord(x)))) / 8)
        self.write_int(self._symbol_length, 4)
        for char in alphabet.keys():
            self.write_symbol(char)

        self.next_section(self._symbol_length)

        for code in alphabet.values():
            self._file_out.write(code.encode("utf-8"))
            self.code_separator()

        self.next_section()

        if len(encoded_data) % 8 != 0:
            encoded_data += '0' * (len(encoded_data) % 8)

        for i in range(0, len(encoded_data), 8):
            self.write_int(int(encoded_data[i:i + 8], 2), 1)
            if self._progress_callback is not None and i % 20 == 0:
                self._progress_callback(length, i)


class ShannonDecoding:
    def __init__(self, file_in: typing.IO, file_out: typing.IO, progress_callback):
        self._file_in = file_in
        self._file_out = file_out
        self._progress_callback = progress_callback

    def read_int(self, length):
        return int.from_bytes(self._file_in.read(length), 'little')

    def chunks(self, length):
        total = 0

        while total < length:
            data = self.read_int(1)
            chunk = bin(data)[2:].rjust(8, '0')
            if total + len(chunk) > length:
                yield chunk[:length % 8]
                return
            yield chunk
            total += len(chunk)

    def get_char(self, idx: int):
        return chr(idx)

    def read(self):
        data_length = self.read_int(4)
        symbol_length = self.read_int(4)
        alphabet = dict()

        symbols = bytes()
        while not symbols.endswith((chr(0) * symbol_length).encode("utf-8")):
            symbols += self._file_in.read(symbol_length)
        symbols = symbols.replace((chr(0) * symbol_length).encode("utf-8"), bytes())

        for i in range(0, len(symbols), symbol_length):
            alphabet[self.get_char(int.from_bytes(symbols[i:i + symbol_length], 'little'))] = ''

        keys = list(alphabet.keys())
        code = bytes()
        i = 0
        while code != chr(0).encode('utf-8'):
            code += self._file_in.read(1)

            if code.endswith(chr(1).encode('utf-8')):
                code = code.replace(chr(1).encode('utf-8'), bytes())
                key = keys[i]
                alphabet[key] = code.decode('utf-8')

                code = bytes()
                i += 1

        codes = {code: letter for letter, code in alphabet.items()}

        current_code = ''
        for chunk in self.chunks(data_length):
            for char in chunk:
                current_code += char
                if current_code in codes.keys():
                    self._file_out.write(codes[current_code])
                    current_code = ''
