import twint 
import os

LIMIT = 100
include_links = 0

def download_tweets(username):
    output = username.lower()

    config = twint.Config()
    config.Format = '{tweet}'
    config.Hide_output = True
    config.Limit = LIMIT
    config.Links = 'include' if include_links else 'exclude'
    config.Output = output
    config.Username = username

    if os.path.isfile(output):
        open(output, 'w').close()

    print(f'Downloading tweets for @{username}...')
    twint.run.Search(config)
    print(f'Downloaded tweets to {output}.')

download_tweets('officialmcafee')