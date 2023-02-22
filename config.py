import tweepy
import praw


def authenticate_twitter_user():
    auth = tweepy.OAuth1UserHandler(
        consumer_key="[TWITTER CONSUMER KEY]",
        consumer_secret="[TWITTER CONSUMER SECRET]",
        access_token="[TWITTER ACCESS TOKEN]",
        access_token_secret="[TWITTER ACCESS TOKEN SECRET]",
    )
    return auth


def authenticate_reddit_user():
    reddit = praw.Reddit(
        client_id="[CLIENT ID]",
        client_secret="[CLIENT SECRET]",
        password="[PW]",
        user_agent="[AGENT]",
        username="[USERNAME]",
    )
    return reddit


def get_openai_key():
    key = "[OPENAI KEY]"
    return key
