'''
    TODO:
        - Somehow add apostrophes between the two words
        - Implement new generator with NLTK
'''

import sentence_generator as sg
import get_tweets as gt
import sys
import re

MARKOV_LENGTH = 2

# higher limit = more unique sentences but slower, lower limit = less unique but faster
LIMIT = 500

# True = to remove, False = not to remove
REMOVE_USERNAMES = True
REMOVE_HASHTAGS = True

# Compare words independent of their capitalization.
def fix_caps(word):
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

# removes words that may mess up the structure of the sentences
def process(data):
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
            elif REMOVE_USERNAMES:
                if '@' in splitdata[s][w]:
                    splitdata[s].remove(splitdata[s][w])
                    w -= 1
            elif REMOVE_HASHTAGS:
                if '#' in splitdata[s][w]:
                    splitdata[s].remove(splitdata[s][w])
                    w -= 1
            w += 1
        
        # join tweet back
        splitdata[s] = " ".join(splitdata[s])

    newdata = " ".join(splitdata)

    return newdata

# Returns the contents of the file, split into a list of words and punctuation.
def word_list(filename):
    with open(filename, 'r') as file:
        data = file.read()

    data = process(data)

    wordlist = [fix_caps(w) for w in re.findall(r"[\w']+|[.,!?;]", data)]
    return wordlist

def main():
    while True:
        username = input("Enter a (public) user, no @ included (e.g potus): ")

        try:
            gt.download_tweets(username, LIMIT)
            break
        except ValueError:
            print("User not found or user is private.")

    words = word_list(username)

    while True:
        print()
        try:
            sg.generate(words, MARKOV_LENGTH)
        # will happen when sentence generator attempts to pop off words an empty list, i.e. not enough tokens
        except (IndexError, FileNotFoundError):
            print("Not enough tweets/words from user to generate a unique output.")
            sys.exit()

        print()
        opt = input("Enter 'Y' to generate another sentence based off the user's tweets, enter anything else to exit: ")

        if opt.lower() == 'y':
            continue

        break
    
if __name__ == "__main__":
    main()