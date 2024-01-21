from openai import OpenAI
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(api_key='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')

DEFAULT_PROMPT = """Please retrieve title, invoive number, issue_date, total amount and table.   
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
    Note that even the date should be in the format DD/MM/YYYY with numeric values.
    If you can't find the information from this article 
    then return "". Do not make things up. 
"""

with open("jsons.txt", "a") as file:

    image_local = './test/files/0b6fcb50-b157-4457-b3a3-06779f91b8b8.jpg'
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

