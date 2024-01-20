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


def image_render(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def image_to_text(gray_image):
    text = pytesseract.image_to_string(gray_image)
    return text

def image_to_bounding_box(gray_image):
    h, w, _ = gray_image.shape
    boxes = pytesseract.image_to_boxes(gray_image)
    for box in boxes.splitlines():
        b = box.split()
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(gray_image, (x, h - y), (x2, h - y2), (0, 255, 0), 2)

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
