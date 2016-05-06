import re
import sys
from itertools import cycle, count

FILE = 1
INVALID_EXT1 = '.exe'
INVALID_EXT2 = '.bat'
REPLACE_ED = 'd'
REPLACE_ER = 'xor'
REPLACE_F = 'ph'
REPLACE_A = '&'
L33T_LIST = ['d00d', 'w00t', 'sk1llz', 'h4xx', 'n0sc0p3', 'pwn4g3', 'r0f1']
A = 2.5
B = 2.5
C = 5
SEED = 1
INCREMENT = 1
WORD_DELIM = ' '
LINE_DELIM = '\n'
OUTPUT = 'n00b.txt'


def extract_l33t():
    repeat_l33t = cycle(L33T_LIST)
    for word in repeat_l33t:
        yield word


def generate_int():
    n = SEED
    while n:
        yield int(A*n*n + B*n + C)
        n += INCREMENT


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

process_ed = re.compile(r'''ed  # Match the characters 'ed'
                            \b  # Match only at the end of a word boundary''', re.X)

process_er = re.compile(r'''er  # Match the characters 'er'
                            \b  # Match only at the end of a word boundary''', re.X)

process_a = re.compile(r'''(and|ant|anned) #Match the three substrings anywhere in string
                                ''', re.X)

process_f = re.compile(r'''\b   # Match at the beginning of a word boundary
                            f   # Match for the character 'f' ''', re.X)

f = open(filename, 'r')
o = open(OUTPUT, 'w')

word_count = 0
insert = generate_int()
w0rd = extract_l33t()
index = next(insert)

for line in f:
    replaced_ed = process_ed.sub(REPLACE_ED, line)
    replaced_er = process_er.sub(REPLACE_ER, replaced_ed)
    replaced_a = process_a.sub(REPLACE_A, replaced_er)
    replaced_f = process_f.sub(REPLACE_F, replaced_a)

    split_string = replaced_f.split()
    line_len = len(split_string)
    print(line_len)
    word_count += line_len
    print(word_count)
    if word_count >= index:
        split_string.insert(index, next(w0rd))
        index = next(insert)

    output_line = WORD_DELIM.join(split_string)
    o.write(output_line)
    o.write(LINE_DELIM)

f.close()
o.close()