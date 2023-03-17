import os
import tweepy
import time

# Replace with your own API keys and access tokens
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to the Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Handle Twitter API rate limits
def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

# Main function to retweet liked tweets
def retweet_elad_gil_likes():
    elad_gil_screen_name = 'eladgil'
    elad_gil_id = api.get_user(screen_name=elad_gil_screen_name).id_str

    for like in limit_handler(tweepy.Cursor(api.favorites, id=elad_gil_id).items()):
        try:
            print(f'Retweeting tweet ID {like.id}')
            api.retweet(like.id)
            time.sleep(60)  # Pause for 1 minute to avoid aggressive retweeting
        except tweepy.TweepError as e:
            print(f'Error while retweeting: {e}')

if __name__ == '__main__':
    retweet_elad_gil_likes()
