import pandas as pd
import numpy as np


def read_files(file_lst: list) -> pd.DataFrame:
    """
    Reads a list of .csvs and puts them into a dataframe.
    """
    df_lst = [pd.read_csv(file) for file in file_lst]  # Reads in the csvs
    combination = pd.concat(df_lst)  # Combines the csvs
    return combination


# Creating the df based on list of csvs
file_lst = ["reddit_data.csv", "tweets.csv"]
combination_df = read_files(file_lst)
combination_df.to_csv("finetune_data.csv", index=False)
print(combination_df)
