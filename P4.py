import re
import sys

FILE = 1
INVALID_EXT1 = '.exe'
INVALID_EXT2 = '.bat'
REPLACE_ED = 'd'
REPLACE_ER = 'xor'

try:
    filename = sys.argv[FILE]

except IndexError:
    print('Pass a text files as a command line argument:')
    print('P4.py <file1>.txt')
    sys.exit()

valid_filename = re.search(r'''^                    # start of filename
                               (?P<name>\w+)        # one or more characters for file name
                               (?P<extension> \.    # one dot to designate file extension
                               \w{2,3})             # exactly two or three characters for file extension
                               $
 ''', filename, re.X)

invalid_extensions = [INVALID_EXT1, INVALID_EXT2]

if valid_filename.group('extension') in invalid_extensions:
    print("Error! Illegal file extension. Do not use:")
    for ext in invalid_extensions:
        print(ext)
    sys.exit()

f = open(filename, 'r')
string = f.read()
f.close()

process_ed = re.compile(r'''ed  # Match the characters 'ed'
    \b  # Match only at the end of a word boundary''', re.X)

process_er = re.compile(r'''er  # Match the characters 'er'
                            \b  # Match only at the end of a word boundary''', re.X)

replaced_ed = process_ed.sub(REPLACE_ED, string)
replaced_er = process_er.sub(REPLACE_ER, replaced_ed)

print(replaced_er)