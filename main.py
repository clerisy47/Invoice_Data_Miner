from openai import OpenAI
from openai_key import OPENAI_KEY
import json
import pandas as pd 
import pytesseract
import cv2
import base64


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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_render(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def image_to_text(gray_image):
    text = pytesseract.image_to_string(gray_image)
    return text

def image_to_bounding_box(gray_image):
    h, w = gray_image.shape
    boxes = pytesseract.image_to_boxes(gray_image)
    for box in boxes.splitlines():
        b = box.split()
        x, y, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(gray_image, (x, h - y), (x2, h - y2), (0, 255, 0), 2)



image = image_render("test/files/0b6fcb50-b157-4457-b3a3-06779f91b8b8.jpg")
# text = image_to_text(image)
boxes = image_to_bounding_box(image)
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()