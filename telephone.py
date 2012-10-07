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
    # Build a dictionary that maps digits to the letters 
    orphans = {'s': 7, 'z': 9}
    letters = string.lowercase

    for orphan in orphans:
        letters = letters.replace(orphan, '')

    numpad = {idx: ''.join(chunk) for idx, chunk in
              enumerate(grouper(3, letters), start=2)}
    numpad[1] = ' '

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

def word_to_digits(words):
    """Inverts a {<word>: <digits>} map."""
    return {v: k for k, v in words.items()}
    
def index_words(index=None):
    if not index:
        index = letter_to_digit_index()
        
    # Map words to how they would be entered on the keypad
    words_index = defaultdict(lambda: '')
    with open('words.txt') as f:
        words = (w.strip('\n').lower() for w in f.readlines())
    
    for word in words:
        for letter in word:
            words_index[word] += str(index[letter])

    return words_index

def stems(s, min_length=1):
    return (s[:r] for r in range(min_length, len(s) + 1))

def dict_of_stems():
    """
    Return a standard index of digital representations of words and its
    stems.

    """
    return {d: stems(d) for d in index_words().values()}

def invert_index():
    try:
        with open('stems.json', 'r') as f:
            stems = json.load(f)
    except:
        build_indices()
            
    index = defaultdict(list)
    for k, v in stems.items():
        for substr in v:
            index[substr].append(k)

    return index

def find_matches(s):
    """
    Return all word matches possible given a digital string representative
    of input from a phone keypad, i.e. text messaging.
    
    :substr: A digital string.
    
    """
    numpad = buttonmap()
    l2d = letter_to_digit_index(numpad)
    words = index_words(l2d)
    inverted_words = word_to_digits(words)
    return [inverted_words[match] for match in invert_index()[s]]

def build_indices():
    with open('numpad.json', 'w') as f:
        json.dump(buttonmap(), f)

    with open('stems.json', 'w') as f:
        stems = dict_of_stems()
        for k, v in stems.items():
            stems[k] = list(v)
        json.dump(stems, f)

    with open('inverted_stems.json', 'w') as f:
        json.dump(dict(invert_index()), f)

    
