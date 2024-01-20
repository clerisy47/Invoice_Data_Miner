import openapi
from openapi_key import openapi_key
import json
import pandas as pd 

DEFAULT_PROMPT = """


"""
MODEL = "gpt-3.5-turbo"


def main(text):
    final_prompt = DEFAULT_PROMPT + text
    response = openapi.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"user", "content": final_prompt}],
    )
    content = response.messages[0]["content"]
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, IndexError):
        pass