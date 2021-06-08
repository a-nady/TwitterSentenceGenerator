'''
    TODO:
        - Somehow add apostrophes between the two words
        - Implement new generator with NLTK
'''


import sentence_generator as sg
import get_tweets as gt
import sys

MARKOV_LENGTH = 2

# higher limit = more unique sentences but slower, lower limit = less unique but faster
LIMIT = 500

# 1 = to remove, 0 = not to remove
REMOVE_USERNAMES = 1
REMOVE_HASHTAGS = 1

def main():
    while 1:
        username = input("Enter a (public) user, no @ included (e.g elonmusk): ")

        try:
            gt.download_tweets(username, LIMIT)
            break
        except ValueError:
            print("User not found or user is private.")

    while 1:
        print()
        try:
            sg.generate(username, MARKOV_LENGTH, REMOVE_USERNAMES, REMOVE_HASHTAGS)
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