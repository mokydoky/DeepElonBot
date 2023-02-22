import openai
import os
from config import get_openai_key

os.environ["OPENAI_API_KEY"] = get_openai_key()


def create_model(jsonl_file, model_name):
    """
    Creates a model using the OpenAI API.
    ---
    Parameters: None
    ---
    Returns: None
    """
    # Defines the command to be run
    command = 'openai api fine_tunes.create -t "{jsonl_file}" -m ada \
--suffix "{model_name}"'.format(
        jsonl_file=jsonl_file, model_name=model_name
    )
    os.system(command)
    return


# Change file names here
jsonl_file = "finetune_data_prepared.jsonl"
model_name = "ada:DeepTwitterV2_2023-2-20"
create_model(jsonl_file, model_name)
