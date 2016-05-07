# AUTHOR: Colin Brinton
# FILENAME: P4.py
# DATE: 05/07/2016
# REVISION HISTORY: 1.0

# DESCRIPTION:
# This program is designed to translate file given via command line argument into l33tspeak. The program will reject
# the file extensions '.exe' and '.bat' for safety purposes. The program will run the following translations steps:
#   1) Replace "ant", "and", "anned" with "&" (i.e. anthill -> &hill;  sandpaper -> s&paper)
#   2) Change all words ending in "ed" to "d" (i.e. talked -> talkd)
#   3) Change all words ending in "er" to "xor" (i.e. runner -> runnxor)
#   4) Change all words starting with "f" to "ph" (i.e. famous -> phamous)
# In addition, the program will insert a word from a given list of l33t words after (10, 20, 35, 55, 80, 110...)
# words from the start of the input file. The appropriate l33t word is selected from the list via a cyclic generator.
# It was discovered that the sequence 10, 20, 35, 55, 80, 110... may be described by the equation:
#   y = 2.5x^2 + 2.5x + 5
# Thus, this equation is used in the implementation of the forward generator.
# The program will retain the general formatting of the original input file.

# ASSUMPTIONS:
# It is assumed that l33t words should be inserted according to the sequence 10, 20, 35, 55, 80, 110...
#   counting from the beginning of the input file. In other words, the first l33t word will be inserted after 10
#   words from the beginning of the input file. The second l33t word will be inserted after 20 words from the
#   beginning of the input file... as opposed to counting 20 words after the first l33t word is inserted.
# It is assumed that the input file is in standard english and that no parts of the file are already in l33tspeak.
#   The program will ignore words with numbers or symbols in them when determining how many words to count before
#   inserting the next l33t word. The above not apply to contractions. (i.e. "hasn't", "don't" are still counted
#   as words)
# Because the substitution requirements of the program appear as "a, b, c, d" and not "1, 2, 3, 4" it is assumed
#   that optimal order to run the substitutions is not necessarily "a, b, c, d". Therefore, the substitutions are
#   done in the order outlined in the description above to address the following problems:
#       1) If the "ed" -> "d" substitution is done before the "&" substitutions words like "cleaned" and "loaned"
#           will lose their meaning. "cleaned" will become "cle&" and "loaned" will become "lo&" It is assumed that
#           in these cases "cleand" and "loand" are preferred.
#       2) If the "ed" -> "d" substitution is done before the "&" substitutions, the "anned" -> "&" substitution will
#           never occur! In this order "banned" will become "bannd" instead of "b&". It is assumed that the
#           "anned" -> "&" is preferred in this case.

from re import search, compile, split, X
from sys import argv, exit
from itertools import cycle

# Used for opening and validating input file, output file
FILE = 1
INVALID_EXT1 = '.exe'
INVALID_EXT2 = '.bat'
OUTPUT = 'n00b.txt'

# Used for substitution
REPLACE_ED = 'd'
REPLACE_ER = 'xor'
REPLACE_F = 'ph'
REPLACE_A = '&'

# Used in generators
L33T_LIST = ['d00d', 'w00t', 'sk1llz', 'h4xx', 'n0sc0p3', 'pwn4g3', 'r0f1']
A = 2.5  # Equation for parabola y = Ax^2 + Bx + C
B = 2.5
C = 5
SEED = 1
INCREMENT = 1

# Used for formatting output
JOIN_DELIM = ''
WORD_DELIM = ' '
CONTRACTION_DELIM = '\''
CONTRACTION_ADJUST = 2


# Cyclic generator to determine l33t word to insert
def extract_l33t():
    repeat_l33t = cycle(L33T_LIST)
    for word in repeat_l33t:
        yield word


# Forward generator to determine l33t word placement
def generate_int():
    n = SEED
    while True:
        yield int(A*n*n + B*n + C)  # Sequence of given integers may be described by a parabolic equation
        n += INCREMENT


# Make sure a command line argument is included
try:
    filename = argv[FILE]

except IndexError:
    print('Pass a text files as a command line argument:')
    print('P4.py <file1>.txt')
    exit()

# Validate file extension
valid_filename = search(r'''^                    # start of filename
                               (?P<name>\w+)        # one or more characters for file name
                               (?P<extension> \.    # one dot to designate file extension
                               \w{2,3})             # exactly two or three characters for file extension
                               $
 ''', filename, X)

invalid_extensions = [INVALID_EXT1, INVALID_EXT2]

if valid_filename.group('extension') in invalid_extensions:
    print("Error! Illegal file extension. Do not use:")
    for ext in invalid_extensions:
        print(ext)
    exit()

# Regular expressions to carry out the "translation"
process_ed = compile(r'''ed  # Match the characters 'ed'
                            \b  # Match only at the end of a word boundary''', X)

process_er = compile(r'''er  # Match the characters 'er'
                            \b  # Match only at the end of a word boundary''', X)

process_a = compile(r'''(and|ant|anned) #Match the three sub-strings anywhere in string
                                ''', X)

process_f = compile(r'''\b   # Match at the beginning of a word boundary
                            f   # Match for the character 'f' ''', X)

# Extract data from file
f = open(filename, 'r')
string = f.read()
f.close()

# Do substitutions in the following order
replaced_a = process_a.sub(REPLACE_A, string)
replaced_ed = process_ed.sub(REPLACE_ED, replaced_a)
replaced_er = process_er.sub(REPLACE_ER, replaced_ed)
replaced_f = process_f.sub(REPLACE_F, replaced_er)

# Create and initialize generator objects
insert = generate_int()
w0rd = extract_l33t()
index = next(insert)

# Split the input string using re to maintain whitespace formatting
split_string = split(r'(\w+)', replaced_f)

# Initialize counters for text parsing
space_count = 0
word_count = 0

# Loop to find and insert l33t words in appropriate locations
for word in split_string:
    if word.isalpha():
        word_count += 1
    elif REPLACE_A in word:  # Words with '&' should not be skipped because substitutions have already been done
        word_count += 1
    else:
        space_count += 1

    # After the generator returned number of words is reached, insert l33t word
    if word_count == index:
        w0rd_formatted = WORD_DELIM + next(w0rd)
        location = index + space_count

        # Adjustment to resolve the case where a contraction (i.e. hasn't, don't) is the index word
        if split_string[location] == CONTRACTION_DELIM:
            location += CONTRACTION_ADJUST
        split_string.insert(location, w0rd_formatted)
        index = next(insert)

# Output the processed input to the given text file
o = open(OUTPUT, 'w')
output = JOIN_DELIM.join(split_string)
o.write(output)
o.close()