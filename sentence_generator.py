import re
import random

# Used briefly while first constructing the normalized mapping
tempMapping = {}

# (tuple of words) -> {dict: word -> *normalized* number of times the word appears following the tuple}
# Example entry:
# ('eyes', 'turned') => {'to': 0.66666666, 'from': 0.33333333}
mapping = {}

# Contains the set of words that can start sentences
starts = []


# tempMapping (and mapping) both match each word to a list of possible next words.
def add_to_mapping(history, word):
    global tempMapping

    while len(history) > 0:
        first = tuple(history)

        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0

        history = history[1:]

# Building and normalizing the mapping.
def build_mapping(wordlist, markovLength):
    global tempMapping
    starts.append(wordlist [0])

    for i in range(1, len(wordlist) - 1):
        if i <= markovLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - markovLength + 1 : i + 1]

        follow = wordlist[i + 1]

        # if the last elt was a period, add the next word to the start list
        if history[-1] == "." and follow not in ".,!?;":
            starts.append(follow)
        add_to_mapping(history, follow)

    # Normalize the values in tempMapping, put them into mapping
    for first, followset in tempMapping.items():
        total = sum(followset.values())

        # Normalizing here:
        mapping[first] = dict([(k, v / total) for k, v in followset.items()])

# Returns the next word in the sentence (chosen randomly)
def next(prevList):
    sum = 0.0
    retval = ""
    index = random.random()

    # Shorten prevList until it's in mapping
    while tuple(prevList) not in mapping:
        prevList.pop(0)

    # Get a random word from the mapping, given prevList
    for k, v in mapping[tuple(prevList)].items():
        sum += v

        if sum >= index and retval == "":
            retval = k

    return retval

def gen_sentence(markovLength):
    # Start with a random "starting word"
    curr = random.choice(starts)
    sent = curr.capitalize()
    prevList = [curr]

    # Keep adding words until we hit a period
    while (curr not in "."):
        curr = next(prevList)
        prevList.append(curr)

        # if the prevList has gotten too long, trim it
        if len(prevList) > markovLength:
            prevList.pop(0)

        if (curr not in ".,!?;"):
            sent += " " # Add spaces between words (but not punctuation)
        sent += curr

    return sent

def generate(words, markovLength):
    build_mapping(words, markovLength)
    print(gen_sentence(markovLength))


