import argparse
import os
from coders.caesar import CaesarEncryptor, CaesarDecryptor
from consts import RED, RESET
from datetime import datetime



def timeit(function):
    def wrapper(*args, **kwargs):
        from datetime import datetime
        start = datetime.now()
        function(*args, **kwargs)
        end = datetime.now()

        duration = end - start
        print(f'\nВзлом завершен за {RED}{duration.total_seconds()}{RESET} секунд')

    return wrapper


parser = argparse.ArgumentParser(description='Encoder | Decoder | By MaxP')
parser.add_argument('-e', '--encode', help='Encode file', type=str)
parser.add_argument('-d', '--decode', help='Decode file', type=str)
parser.add_argument('-k', '--key', help='Key for caesar encryption', type=int)
parser.add_argument('-g', '--gui', help='Run gui', action='store_true')

args = parser.parse_args()
# print(args)
start = datetime.now()
if args.encode:
    path = os.path.join(os.getcwd(), args.encode)
    assert os.path.exists(path), 'Please specify a existing file'
    with open(path, 'r', encoding='utf-8', newline='\n') as file_in:
        with open(path + '.prar', 'wb') as file_out:
            CaesarEncryptor(file_in, file_out, None, args.key if args.key is not None else 0).write()
elif args.decode:
    path = os.path.join(os.getcwd(), args.encode)
    assert os.path.exists(path), 'Please specify a existing file'
    assert '.prar' in args.decode, 'Please specify a .prar file'
    with open(path, 'rb') as file_in:
        with open(path.replace('.prar', ''), 'w', encoding='utf-8', newline='\n') as file_out:
            start = datetime.now()
            CaesarDecryptor(file_in, file_out, None, args.key if args.key is not None else 0).read()
            end = datetime.now()
            duration = end - start
            print(f'Decoding finish in {RED}{duration.total_seconds()}{RESET} seconds')
elif args.gui:
    import gui
    gui.main()
else:
    print('Please use only one argument')
end = datetime.now()
duration = end - start
print(f'\nFinished task in {RED}{duration.total_seconds()}{RESET} seconds')


