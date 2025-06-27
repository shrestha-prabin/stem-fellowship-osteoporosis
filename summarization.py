import os
import re

import markdown
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


def create_prompt(context):
    return f"""Read the patient information provided below. Write a short, clear summary for the 
    patient to easily understand. Use only the information given — do not add, assume, 
    or invent any details. Use simple sentences and avoid medical jargon. Include only 
    the key facts about fractures, scans, menopause or reproductive status, family 
    history, lifestyle habits (smoking, alcohol, falls), important supplements or 
    medications, major medical conditions, and surgeries exactly as stated. Limit the 
    summary to 4-6 short sentences. Do not interpret, explain, or fill in missing 
    information. Use only what is written.

    PATIENT INFORMATION:
    Here is the patient data:

    After your're done, give 3 possible solutions to mitigate the risk of the disease and promote life longevity.
    
    {context}
    =====
    """


def generate_summary(model, provider, query):
    client = InferenceClient(
        provider=provider,
        api_key=os.environ["HF_TOKEN"],
    )

    messages = [
        {
            "role": "user",
            "content": create_prompt(query),
        }
    ]

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        # max_tokens=500,
        stream=True,
    )

    try:
        full_response = ""

        for chunk in stream:
            if "choices" in chunk:
                content_piece = chunk.choices[0].delta.content
                if content_piece:
                    full_response += content_piece

        print(model)
        print(full_response)
        return markdown.markdown(full_response)

        # full_response = full_response.replace("\n", "")

        # full_response = re.sub(r"(<think>.*<\/think>)", "", full_response).strip()
        return full_response
        # if response.choices is not None:
        #     return response.choices[0].message.content
        # if response.statuscode == 503:
        #     return response.message
    except Exception as ex:
        print(ex)
        return "Something went wrong"


def generate_summary_deepseek(query):
    API_URL = "https://cwsczdtu0d9jkqor.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        "Content-Type": "application/json",
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    prompt = create_prompt(
        "The patient has reported a history of hip fracture Yes, spine fracture No, and other adult fractures Yes, with the fracture occurring at the age of 52. The specific bone that was fractured was the Pelvis, Ankle and Foot Bones. A DEXA scan has previously been performed No, with the most recent scan details noted as . The patient has experienced a fragility fracture after age 45 No and a low-trauma fracture at a younger age No. In terms of reproductive history, the patient is currently in menopause No, which began at the age of 80, and is classified as Yes menopause. The ovaries have been removed No. There is a family history of osteoporosis No and a parental history of hip fracture No. The patient's smoking status is currently No, with a history of smoking described as No. Alcohol intake is noted as excessive: No, and there is a history of falls No. The patient also has a history of No. Nutritional intake includes a high-calcium diet Yes, along with the use of calcium supplements Yes and vitamin D supplements Yes. Medically, the patient has a history of long-term steroid use No, estrogen therapy No, and has taken osteoporosis medications Yes. The SSRI usage for the patient is No and PPI usage is No. Relevant medical conditions include rheumatoid arthritis No, hyperthyroidism No, Crohn’s or celiac disease No, kidney disease or dialysis No, COPD No, HIV/AIDS No, depression No, and diabetes No. The patient has recently experienced weight loss No and height loss No, and has undergone spine surgery No or hip surgery No or gastric surgery No. Lastly, it is noted whether the patient is currently pregnant No."
    )
    output = query(
        {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 500},
        }
    )

    output = output[0]["generated_text"].split("=====")[-1]

    print(output)
    return output
