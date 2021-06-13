import os
import sys
# use modified twint
sys.path.insert(0, 'src/twint')
import twint 


include_links = 0

def download_tweets(username, limit):
    output = username.lower()

    config = twint.Config()
    config.Format = '{tweet}'
    config.Hide_output = True
    config.Limit = limit
    config.Links = 'include' if include_links else 'exclude'
    config.Output = output
    config.Username = username

    if os.path.isfile(output):
        open(output, 'w').close()
        
    print(f'Downloading tweets for @{username}...')
    twint.run.Search(config)
    print(f'Downloaded tweets to {output}.')

