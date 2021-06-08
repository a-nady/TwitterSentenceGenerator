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

# Compare words independent of their capitalization.
def fixCaps(word):
    # Ex: "FOO" -> "foo"
    if word.isupper() and word != "I":
        word = word.lower()
        # Ex: "LaTeX" => "Latex"
    elif word [0].isupper():
        word = word.lower().capitalize()
        # Ex: "wOOt" -> "woot"
    else:
        word = word.lower()
    return word

# hash tuples from dicts
def toHashKey(lst):
    return tuple(lst)

# removes words that may mess up the structure of the sentences
def process(data, usernames, hashtags):
    splitdata = data.split("\n")

    for s in range(len(splitdata)):
        splitdata[s] = splitdata[s].split(" ")
        w = 0
        # while loop since len changes if removal occurs
        while w < len(splitdata[s]):
            # clutter from scraping
            if splitdata[s][w] == "&amp;":
                    splitdata[s].remove(splitdata[s][w])
                    w -= 1
            elif usernames:
                if '@' in splitdata[s][w]:
                    splitdata[s].remove(splitdata[s][w])
                    w -= 1
            elif hashtags:
                if '#' in splitdata[s][w]:
                    splitdata[s].remove(splitdata[s][w])
                    w -= 1
            w += 1
        
        # join tweet back
        splitdata[s] = " ".join(splitdata[s])

    newdata = " ".join(splitdata)

    return newdata

# Returns the contents of the file, split into a list of words and punctuation.
def wordlist(filename, usernames, hashtags):
    f = open(filename, 'r')
    data = f.read()
    f.close()

    data = process(data, usernames, hashtags)

    wordlist = [fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", data)]
    return wordlist

# tempMapping (and mapping) both match each word to a list of possible next words.
def addItemToTempMapping(history, word):
    global tempMapping
    while len(history) > 0:
        first = toHashKey(history)
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
def buildMapping(wordlist, markovLength):
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
        addItemToTempMapping(history, follow)
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
    while toHashKey(prevList) not in mapping:
        prevList.pop(0)
    # Get a random word from the mapping, given prevList
    for k, v in mapping[toHashKey(prevList)].items():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return retval

def genSentence(markovLength):
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

def generate(file, markovLength, users, htags):
    buildMapping(wordlist(file, users, htags), markovLength)
    print(genSentence(markovLength))


