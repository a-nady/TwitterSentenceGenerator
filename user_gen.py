import sentence_generator as sg
import get_tweets as gt

MARKOV_LENGTH = 2
LIMIT = 100
# just testing
gt.download_tweets('elonmusk', 1000)
sg.generate('elonmusk', 3)