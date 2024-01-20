import openapi
from openapi_key import openapi_key
import json
import pandas as pd 
import pytesseract
import cv2

DEFAULT_PROMPT = """
Please retrieve title, invoive number, issue_date, total amount and table.   
    Always return your response as a valid JSON string. The format of that string should be this, 
    {
        invoice_number: RSN/18-19/4126,
        invoice_number_bbox: [608, 130, 720, 142],
        invoice_date: 09/03/2019,
        total: 76900,
        table: S Description of Goods HSN/SAC GST Quantity Rate per Disc. % Amount
                Rate
                SAMSUNG S10PLUS 85171290 12 % 1 No. 68,660.71 No. 68,660.71
                512GB G975 CERAMIC BLACK
                Batch : 1 No.
    }
    If you can't find the information from this article 
    then return "". Do not make things up. 
    Here's the raw data from the invoice:
    
"""
MODEL = "gpt-3.5-turbo"


def image_to_text(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    image = cv2.imread(image_path)

    text = pytesseract.image_to_string(image)
    return text

def text_to_df(text):
    final_prompt = DEFAULT_PROMPT + text
    response = openapi.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"user", "content": final_prompt}],
    )
    content = response.messages[0]["content"]
    try:
        data = json.loads(content)
        data = {key: [value] for key, value in data.items()}
        return pd.DataFrame(data)

    except (json.JSONDecodeError, IndexError):
        pass
