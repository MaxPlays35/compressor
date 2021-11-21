from coders.shannon import ShannonEncoding, ShannonDecoding


with open('texts\\oblomov.txt', 'r', encoding='utf-8', newline='\n') as file:
    with open('output.prar', 'wb') as out:
        a = ShannonEncoding(file, out, None)
        # print(a.get_alphabet())
        a.write()

with open('out.txt', 'w', encoding='utf-8', newline='\n') as file:
    with open('output.prar', 'rb') as file2:
        a = ShannonDecoding(file2, file, None)
        a.read()
