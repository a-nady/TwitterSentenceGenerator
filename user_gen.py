import sentence_generator as sg
import get_tweets as gt
import sys

MARKOV_LENGTH = 2
LIMIT = 100

def main():
    while 1:
        username = input("Enter a (public) user, no @ included (e.g elonmusk): ")

        try:
            gt.download_tweets(username, LIMIT)
            break
        except ValueError:
            print("User not found")
    
    while 1:
        print()
        try:
            sg.generate('elonmusk', 3)
        # will happen when sentence generator attempts to pop off words an empty list, i.e. not enough tokens
        except IndexError:
            print("Not enough tweets/words from user to generate a unique output.")
            sys.exit()

        print()
        opt = input("Enter 'Y' to generate another sentence based off the user's tweets, enter anything else to exit: ")

        if opt.lower() == 'y':
            continue

        break

main()