import openai
import pandas as pd
from config import get_openai_key
import os

openai.api_key = get_openai_key()


def prepare_data(csv_file:str, json_file:str) -> None:    
    """
    Given a csv file, convert it to jsonl format and uses the OpenAI API to
    prepare the data for fine-tuning.
    """
    data = pd.read_csv(csv_file)
    data.to_json(json_file, orient="records", lines=True)
    command = "openai tools fine_tunes.prepare_data -f {json_file}".format(
        json_file=json_file
    )
    os.system(command)
    return


# Change file names here
csv_file = "finetune_data.csv"
json_file = "finetune_data.jsonl"
prepare_data(csv_file, json_file)
