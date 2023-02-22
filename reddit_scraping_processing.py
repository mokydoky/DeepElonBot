# File for generating prompt/completion csvs from reddit data.
# Choose subreddits and edit name of csv file below.

import praw
import pandas as pd
import numpy as np
from config import authenticate_reddit_user

reddit = authenticate_reddit_user()


class subreddit:
    """
    A class that represents a subreddit. Used for inputting subreddit names
    and listing the functions needed to scrape and process them.
    ---
    attributes:
        name: str
            The name of the subreddit.
        top100: list
            A list of the top 100 posts from the subreddit.
        split_func: function
            The function that splits the top 100 posts into a dataframe of
            prompts and completions.
        list_funcs: list
            A list of functions that process the top 100 posts.
    """

    def __init__(self, name, split_func, list_funcs):
        self.name = name
        self.top100 = list(reddit.subreddit(name).top())
        self.split_func = split_func
        self.list_funcs = list_funcs

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


def title_body_split(subreddit_obj):
    """
    Given a subreddit objectm returns a dataframe of the top 100 posts
    from the subreddit divided by title and body.
    ---
    Parameters:
        subreddit_obj: subreddit
    ---
    Returns: df
    """
    # Creates a list of titles and bodies from the top 100 posts
    titles = [post.title for post in subreddit_obj.top100]
    bodies = [post.selftext for post in subreddit_obj.top100]
    # Creates a dataframe of the titles and bodies
    df = pd.DataFrame()
    df = df.assign(Prompt=titles).assign(Completion=bodies)
    return df


def title_four_words_split(subreddit_obj):
    """
    Given a subreddit object, returns a dataframe of the top 100 posts from the
    subreddit with their title divided by the first four words and the rest.
    ---
    Parameters:
        subreddit_obj: subreddit
    ---
    Returns: df
    """
    # Creates a list of titles from the top 100 posts of each, dropping posts
    # with less than four words
    titles = [
        post.title
        for post in subreddit_obj.top100
        if len((str(post.title)).split()) > 4
    ]
    # Creates a list of the first four words, and a list of the remaining words
    titles_four = [" ".join(post.split()[:4]) for post in titles]
    titles_rest = [" ".join(post.split()[4:]) for post in titles]
    # Creates a dataframe of the titles and bodies
    df = pd.DataFrame()
    df = df.assign(Prompt=titles_four).assign(Completion=titles_rest)
    return df


def removeWP(text):
    """
    Takes a piece of text and removes the "[WP]" from the beginning.
    ---
    Parameters:
        text: str
    ---
    Returns: str
    """
    return text.removeprefix("[WP]")


def remove_edits(text):
    """
    Takes a piece of text and removes anything past an edit
    ---
    Parameters:
        text: str
    ---
    Returns: str
    """
    check_list = ["edit: ", "EDIT: ", "Edit: ", "Edit1: "]
    for check in check_list:
        if check in text:
            return text.split(check)[0]
    return text


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


# Make a list of subreddits and their functions (CAN ADD MORE WHENEVER)
lst_subreddits = [
    subreddit(name="Jokes", split_func=title_body_split, list_funcs=[remove_edits]),
    subreddit(
        name="Showerthoughts",
        split_func=title_four_words_split,
        list_funcs=[remove_edits],
    ),
    subreddit(
        name="WritingPrompts",
        split_func=title_four_words_split,
        list_funcs=[remove_edits, removeWP],
    ),
]

# Create a list of dataframes from the subreddits
df_lst = [subredd.create_df() for subredd in lst_subreddits]
# Convert dataframes into the csv
combine_csv(df_lst, "reddit_data.csv")
