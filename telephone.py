import json
import string
from collections import defaultdict
from itertools import chain, combinations, izip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def buttonmap():
    """Build a dictionary that maps digits to the letters."""
    orphans = {'s': 7, 'z': 9, 'S': 7, 'Z': 9}
    letters = ''.join(sorted(string.letters, key=lambda x: x.lower()))

    # Drop out our 'orphan' letters so that we can split our letters into
    # uniformly sized groups. We'll add the orphans back in later.
    for orphan in orphans:
        letters = letters.replace(orphan, '')

    numpad = {idx: ''.join(chunk) for idx, chunk in
              enumerate(grouper(6, letters), start=2)}
    numpad[1] = ' '

    # We're putting our orphans back in their home. :)
    for orphan, i in orphans.items():
        numpad[i] += orphan

    return numpad

def letter_to_digit_index(numpad=None):
    if not numpad:
        numpad = buttonmap()
        
    index = {}
    for digit, letter_group in numpad.items():
        for letter in letter_group:
            index[letter] = digit

    return index

def digits_to_word():
    """Returns a {<digits>: <word>} dict from a text file of words."""
    index = {}
    letters = letter_to_digit_index()
    
    with open('allwords.txt') as f:
        words = (w.strip('\n') for w in f.readlines())

    for word in words:
        key = ''.join(str(letters[l]) for l in word if l in string.letters)
        index[key] = word

    return index

def stems(s, min_length=1):
    """
    Return generator function that yields substrings of 's', starting at
    the 0th index. Each invocation increments the length of the substring
    by 1, e.g.:

    let 's' == '12345'
      yield 0: '1'
      yield 1: '12'
      yield 2: '123'

    etc.

    'min_length' specifies the shortes substring to evaluate.
    
    """
    return (s[:r] for r in range(min_length, len(s) + 1))

def dict_of_stems():
    """
    Return a standard index of digital representations of words and its
    stems, e.g. {'12345': ['1', '12', '123', '1234', '12345']}
    

    """
    return {d: stems(d) for d in digits_to_word()}

def invert_index():
    """
    Invert the dictionary returned by 'dict_of_stems()'. For example:

    let 'dict_of_stems()' = {'12345': ['1', '12', '123', '1234', '12345']
                             '12456': ['1', '12', '124', '1245', '12456']}

      >> invert_index()
      {'1': ['12345', '12456'],
       '12': ['12345', '12456'],
       '123': ['12345'],
       '1234': ['12345'],
       '124': ['12456'],
       '1245': ['12456']}
    
    """
    try:
        with open('stems.json', 'r') as f:
            stems = json.load(f)
    except:
        stems = dict_of_stems()
            
    index = defaultdict(list)
    for k, v in stems.items():
        for substr in v:
            index[substr].append(k)

    return index

def _build_index():
    stemwords = defaultdict(list)
    idx = invert_index()
    digits = digits_to_word()

    for k, v in idx.items():
        for i, val in enumerate(v):
            stemwords[k].append(digits[val])

    return stemwords

def output():
    """Write out JSON data used for persistence."""
    with open('numpad.json', 'w') as f:
        json.dump(buttonmap(), f)

    with open('inverted_index.json', 'w') as f:
        json.dump(_build_index(), f)

def find_matches(s):
    """
    Return all word matches possible given a digital string representative
    of input from a phone keypad, i.e. text messaging.
    
    :substr: A digital string.
    
    """
    with open('inverted_index.json', 'r') as f:
        idx = json.load(f)

    return idx.get(s)

