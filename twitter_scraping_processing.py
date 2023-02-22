# File for generating prompt/completion csvs from twitter data. With new
# Twitter API changes, this file is not useable without spending a lot of
# money that I don't have.

# Old tweets.csv is used instead.

import tweepy
import pandas as pd
import numpy as np
from config import authenticate_twitter_user

auth = authenticate_twitter_user()
api = tweepy.API(auth)


class twitter_user:
    """
    A class that represents a twitter user. Used for inputting twitter ids
    and listing the functions needed to scrape and process them.
    ---
    attributes:
        id: str
            The id of the twitter user.
        split_func: function
            The function that splits the tweets into a dataframe of prompts
            and completions.
        list_funcs: list
            A list of functions that process the tweets.
        tweetbodies: list of str
            A list of the tweets from the user.
    """

    def __init__(self, id, split_func, list_funcs):
        # setting max count to 3200 to get the most tweets possible
        max_count = 3200
        # setting max repeats to 16 to get as many tweets as the API allows
        max_repeats = 16
        self.id = id
        self.split_func = split_func
        self.list_funcs = list_funcs
        # set initial list of tweets
        tweets = api.user_timeline(
            user_id=id, count=max_count, exclude_replies=True, include_rts=False
        )
        currmax = tweets[-1].id
        # repeat process until max number of tweets is reached
        for i in np.arange(max_repeats):
            tweets = tweets + api.user_timeline(
                user_id=id,
                count=max_count,
                exclude_replies=True,
                include_rts=False,
                max_id=currmax,
            )
            currmax = tweets[-1].id
            tweets.pop()
        # create list of tweet bodies longer than four words without a link
        self.tweetbodies = [
            tweet.text
            for tweet in tweets
            if len(tweet.text.split()) > 4
            and not tweet.text.str.contains("https")
            and not tweet.text.str.contains("t.co")
        ]

    def create_df(self):
        """
        Creates and processes a dataframe of the top 100 posts from the
        subreddit.
        ---
        Parameters: None
        ---
        Returns: df
        """
        df = self.split_func(self)
        for func in self.list_funcs:
            df["Prompt"] = df["Prompt"].apply(func)
            df["Completion"] = df["Completion"].apply(func)
        return df


def title_four_words_split(twitter_user_obj):
    first_four = [" ".join(tweet.split()[:4]) for tweet in twitter_user_obj.tweetbodies]
    rest = [" ".join(tweet.split()[4:]) for tweet in twitter_user_obj.tweetbodies]
    # Creates a dataframe of the titles and bodies
    df = pd.DataFrame()
    df = df.assign(Prompt=first_four).assign(Completion=rest)
    return df


def combine_csv(df_lst, csv_name):
    """
    Takes a list of dataframes and combines them into one dataframe and exports
    it to a csv.
    ---
    Parameters:
        df_lst: list of dataframes
    ---
    Returns: nothing
    """
    new_df = pd.concat(df_lst)
    new_df.to_csv(csv_name, index=False)
    return


lst_users = [
    twitter_user(id="44196397", split_func=title_four_words_split, list_funcs=[])
]

# Create a list of dataframes from the subreddits
df_lst = [user.create_df() for user in lst_users]
# Convert dataframes into the csv
combine_csv(df_lst, "twitter_data.csv")
