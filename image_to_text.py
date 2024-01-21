from openai import OpenAI
import base64
import csv
from openai_key import OPENAI_KEY
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key=OPENAI_KEY)

DEFAULT_PROMPT = """Please retrieve title, invoive number, issue_date, total amount and table.
    Note that even the date should be in the format DD/MM/YYYY with numeric values.   
    Always return your response as a valid JSON string. The format of that string should be this, 
    {
        invoice_number: RSN/18-19/4126,
        invoice_date: 09/03/2019,
        total: 76900,
        table: S Description of Goods HSN/SAC GST Quantity Rate per Disc. % Amount
                Rate
                SAMSUNG S10PLUS 85171290 12 % 1 No. 68,660.71 No. 68,660.71
                512GB G975 CERAMIC BLACK
                Batch : 1 No.
    }
    If you can't find the information from this article 
    then return "". Do not make things up. Even if the message isn't visible, no need to write apologising messages,
    just return the JSON string.
"""
csv_file_path = 'test/gt.csv'
titles = []

with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        title = row['title']
        titles.append(title)

with open("jsons.txt", "a") as file:

    for title in titles:
        image_local = os.path.join('./test/files', title)
        image_url = f"data:image/jpeg;base64,{encode_image(image_local)}"


        response = client.chat.completions.create(
            model='gpt-4-vision-preview', 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": DEFAULT_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ],
                }
            ],
            max_tokens=500,
        )

        json_string = response.choices[0].message.content
        json_string = json_string.replace("```json\n", "").replace("\n```", "").replace("```", "")

        file.write(json_string+ "\n")

  

