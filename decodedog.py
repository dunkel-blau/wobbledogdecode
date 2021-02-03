import enum, dataclasses
import string

GENE_SEPARATOR = '^'
GENE_LENGTH = 20

SEPARATOR_SEQUENCES = {
    ':': '|00',
    ';': '|01',
    '<': '|10',
    '=': '|11',
    '>': '||0',
    '?': '||1',
    '@': '|0|',
    '[': '|1|',
    '#': '|||',
    ']': '|0',
    '^': '|1',
    '_': '||',
    '*': '|',
}

# requires i < text length
# swaps character in position i with the character
# in a different position based on the ascii value
def interiorScramble(text: str, i: int) -> str:
    length = len(text)
    a = int((text[(i + 1)%length]).encode('utf-8')[0])
    b = (i + a) % length

    # if a%length == 1: # why?
    if (i+1)%length == b: # original test
        return text
    
    scrambled = list(text)
    scrambled[i] = text[b]
    scrambled[b] = text[i]

    return ''.join(scrambled)

def scrambled(text: str) -> str:
    for i in range(len(text)):
        text = interiorScramble(text, i)
    return text

def unscrambled(text: str) -> str:
    for i in range(len(text)):
        text = interiorScramble(text, len(text)-i-1)
    return text

def decodeGeneSymbol(text: str) -> str:
    if not text:
        return ""
    elif len(text) == 1 and text in string.ascii_lowercase:
        return str((string.ascii_lowercase.index(text))+1).rjust(2, '0')
    else:
        return bin(int(text, 16))[2:]

def geneticDecode(text: str) -> str:

    altGeneSize = GENE_LENGTH/4
    decoded = ""
    accumulated = ""

    for idx, c in enumerate(text):
        if c in SEPARATOR_SEQUENCES:
            decoded += decodeGeneSymbol(accumulated)
            decoded += SEPARATOR_SEQUENCES[c]
            accumulated = ""
        elif c in string.ascii_lowercase:
            decoded += decodeGeneSymbol(accumulated)
            decoded += decodeGeneSymbol(c)
            accumulated = ""
        else:
            accumulated += c
            if len(accumulated) == altGeneSize or idx == len(text)-1:
                decoded += decodeGeneSymbol(accumulated)
                accumulated = ""

    return decoded

class DogAge(enum.Enum):
    NONE = 0
    PUPPY = 1
    CHILD = 2
    TEEN = 3
    YOUNG_ADULT = 4
    ADULT = 5

@dataclasses.dataclass
class SavableDog:
    genes: str
    domRecGenes: str
    age: DogAge
    agep: float
    defaultName: str

def decodeDog(dogText: str) -> SavableDog:

    segments = unscrambled(dogText).split(GENE_SEPARATOR)

    genes = geneticDecode(segments[0])

    domrecgenes = geneticDecode(segments[1]) \
        .replace('0', 'a') \
        .replace('1', 'A')

    age = DogAge[segments[2]]

    ageProgress = float(segments[3])

    defaultName = segments[4]

    return SavableDog(genes, domrecgenes, age, ageProgress, defaultName)

if __name__ == '__main__':
    import sys

    try:
        operation = sys.argv[1]
        if not operation in ['decode', 'encode', 'unscramble', 'scramble']:
            raise ValueError
    except (IndexError, ValueError):
        print('Usage: decodedog.py [decode, encode, unscramble, scramble]')
        exit()

    dogText = input("input dog:\n > ")

    print('\nResult:\n')

    if operation == 'decode':
        print(decodeDog(dogText))
    elif operation == 'unscramble':
        print(unscrambled(dogText))
    elif operation == 'scramble':
        print(scrambled(dogText))
    elif operation == 'encode':
        print(unscrambled(dogText))