# TwitterSentenceGenerator

TwitterSentenceGenerator scrapes user's tweets using a (modified) version of twint, applies the markov chain model on that user data to create randomly generated sentences.

# Demo

![Demo](https://i.imgur.com/0qsVbAU.gif)

# About and General Aspects
- Basically it pretends whoever the user is! If the user was a robot with a nice vocabulary but with little understanding of how words would sound next to each other, this is basically how it would look.
- NLTK or other NLP toolkits are not required for this sentence generator (another model in the works with more legibility requires it however) so the program is relatively lightweight.

# Caveats
- User must have ~30-60 tweets (depending on the word count per tweet)
- Internet is required to fetch the user's tweets 
- Even if sentences are syntatically correct, it still sometimes it doesn't make sense. But sometimes it results in absurd sentences that are funny!

# Requirements 
- Python 3.6+
- Twint

# Installation

```bash
git clone https://github.com/a-nady/TwitterSentenceGenerator
```
Go to the directory of the cloned folder in terminal and run
```bash
python3 user_gen.py
```
or use an IDE to open `user_gen.py` and run it.

There are a few things you can configure, the amount of tweets the program should roughly scrape (LIMIT), the markov chain length (MARKOV_LENGTH), and whether to include links, hashtags, and usernames the user replied to or not. Variable Markov lengths result in different sounding sentences so feel free to expirement with it!

Enter the user or yourself (if you have a twitter) to see what a robot version would sound like!
