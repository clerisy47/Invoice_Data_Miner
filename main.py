import openapi
from openapi_key import openapi_key
import json
import pandas as pd 
import pytesseract
import cv2

DEFAULT_PROMPT = """


"""
MODEL = "gpt-3.5-turbo"


def image_to_text(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    image = cv2.imread(image_path)

    text = pytesseract.image_to_string(image)
    return text

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