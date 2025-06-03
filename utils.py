import json
import os
import time

import pandas as pd


def paragraph(data: dict, is_male) -> str:

    with open("./app/static/data.json") as f:
        data_file = json.load(f)

    formatted_answers = [
        {
            "key": "hipFracture",
            "text": f"The patient has reported a history of hip fracture {data['hipFracture'][0]}",
        },
        {"key": "spineFracture", "text": f"Spine fracture {data['spineFracture'][0]}"},
        {
            "key": "otherAdultFracture",
            "text": f"And other adult fractures {data['otherAdultFracture'][0]}",
        },
        {
            "key": "fractureAge",
            "text": f"With the fracture occurring at the age of {data['fractureAge'][0]}",
        },
        {
            "key": "fracturedBones",
            "text": f"The specific bone that was fractured was the {''.join(data['fracturedBones'])}",
        },
        {
            "key": "priorDexaScan",
            "text": f"A DEXA scan has previously been performed {data['priorDexaScan'][0]}",
        },
        {
            "key": "lastDexaScanDetails",
            "text": f"With the most recent scan details noted as {data['lastDexaScanDetails'][0]}",
        },
        {
            "key": "fragilityFractureAfter45",
            "text": f"The patient has experienced a fragility fracture after age 45 {data['fragilityFractureAfter45'][0]}",
        },
        {
            "key": "youngLowTraumaFracture",
            "text": f"And a low-trauma fracture at a younger age {data['youngLowTraumaFracture'][0]}",
        },
        {
            "key": "currentlyInMenopause",
            "text": f"The patient is currently in menopause {data['currentlyInMenopause'][0]}",
        },
        {
            "key": "ageAtMenopause",
            "text": f"Which began at the age of {data['ageAtMenopause'][0]}",
        },
        {
            "key": "menopauseType",
            "text": f"And is classified as {data['menopauseType'][0]} menopause",
        },
        {
            "key": "ovariesRemoved",
            "text": f"The ovaries have been removed {data['ovariesRemoved'][0]}",
        },
        {
            "key": "familyHistoryOsteoporosis",
            "text": f"There is a family history of osteoporosis {data['familyHistoryOsteoporosis'][0]}",
        },
        {
            "key": "familyHistoryHipFracture",
            "text": f"And a parental history of hip fracture {data['familyHistoryHipFracture'][0]}",
        },
        {
            "key": "currentSmoker",
            "text": f"The patient's smoking status is currently {data['currentSmoker'][0]}",
        },
        {
            "key": "everSmoked",
            "text": f"With a history of smoking described as {data['everSmoked'][0]}",
        },
        {
            "key": "excessiveAlcoholIntake",
            "text": f"Alcohol intake is noted as excessive: {data['excessiveAlcoholIntake'][0]}",
        },
        {
            "key": "historyOfFalls",
            "text": f"There is a history of falls {data['historyOfFalls'][0]}",
        },
        {
            "key": "eatingDisorder",
            "text": f"The patient also has a history of {data['eatingDisorder'][0]}",
        },
        {
            "key": "highCalciumDiet",
            "text": f"Nutritional intake includes a high-calcium diet {data['highCalciumDiet'][0]}",
        },
        {
            "key": "calciumSupplements",
            "text": f"Along with the use of calcium supplements {data['calciumSupplements'][0]}",
        },
        {
            "key": "vitaminDSupplements",
            "text": f"And vitamin D supplements {data['vitaminDSupplements'][0]}",
        },
        {
            "key": "longTermSteroids",
            "text": f"The patient has a history of long-term steroid use {data['longTermSteroids'][0]}",
        },
        {
            "key": "takenEstrogen",
            "text": f"Estrogen therapy {data['takenEstrogen'][0]}",
        },
        {
            "key": "osteoporosisMedications",
            "text": f"And has taken osteoporosis medications {data['osteoporosisMedications'][0]}",
        },
        {
            "key": "ssriUse",
            "text": f"The SSRI usage for the patient is {data['ssriUse'][0]}",
        },
        {"key": "ppiUse", "text": f"And PPI usage is {data['ppiUse'][0]}"},
        {
            "key": "rheumatoidArthritis",
            "text": f"Relevant medical conditions include rheumatoid arthritis {data['rheumatoidArthritis'][0]}",
        },
        {
            "key": "hyperthyroidism",
            "text": f"Hyperthyroidism {data['hyperthyroidism'][0]}",
        },
        {
            "key": "crohnsOrCeliac",
            "text": f"Crohn’s or celiac disease {data['crohnsOrCeliac'][0]}",
        },
        {
            "key": "kidneyDiseaseOrDialysis",
            "text": f"Kidney disease or dialysis {data['kidneyDiseaseOrDialysis'][0]}",
        },
        {"key": "copd", "text": f"COPD {data['copd'][0]}"},
        {"key": "hivAids", "text": f"HIV/AIDS {data['hivAids'][0]}"},
        {"key": "depression", "text": f"Depression {data['depression'][0]}"},
        {"key": "diabetes", "text": f"And diabetes {data['diabetes'][0]}"},
        {
            "key": "recentWeightLoss",
            "text": f"The patient has recently experienced weight loss {data['recentWeightLoss'][0]}",
        },
        {
            "key": "recentHeightLoss",
            "text": f"And height loss {data['recentHeightLoss'][0]}",
        },
        {
            "key": "spineSurgery",
            "text": f"And has undergone spine surgery {data['spineSurgery'][0]}",
        },
        {"key": "hipSurgery", "text": f"Or hip surgery {data['hipSurgery'][0]}"},
        {
            "key": "gastricSurgery",
            "text": f"Or gastric surgery {data['gastricSurgery'][0]}",
        },
        {
            "key": "currentlyPregnant",
            "text": f"Lastly, it is noted whether the patient is currently pregnant {data['currentlyPregnant'][0]}",
        },
    ]

    formatted_paragraph = ""

    for answer in formatted_answers:
        is_female_question = False
        for item in data_file:
            if item["name"] == answer["key"] and item.get("femaleOnly") == True:
                is_female_question = True
                break
        if is_female_question and is_male:
            continue

        formatted_paragraph += answer["text"] + ". "
    return formatted_paragraph


def prediction(calculated_weight, total_weight):
    risk_percentage = calculated_weight / total_weight * 100
    return f"The patient is at {risk_percentage:.2f}% risk of osteoporosis"


def export_form_data(form_data):
    result = []
    with open("./app/static/data.json", encoding="utf-8") as f:
        form_meta = json.load(f)

        output_data = {}
        input_weight = 0
        total_weight = 0

        for form_item in form_meta:
            col = form_item["name"]

            if form_item.get("femaleOnly") and form_data.get("gender") == "Male":
                output_data[col] = [""]
                continue

            selected_values = []
            if form_item.get("type") == "multiselect":
                selected_values = form_data.getlist(col)
                value = ", ".join(selected_values)
            else:
                value = form_data.get(col)

            weight = 0
            if form_item.get("type") == "boolean":
                if value == "Yes":
                    weight = form_item["weight"]

            elif form_item.get("type") == "select":
                if value is not "--None--":
                    weight = form_item["weight"]
            elif form_item.get("type") == "multiselect":
                if len(selected_values) > 0:
                    weight = form_item["weight"]
            else:
                if len(value) > 0:
                    weight = form_item["weight"]

            input_weight += weight
            total_weight += form_item["weight"]

            print(col, value)
            output_data[col] = [value]
            result.append({"q": form_item["question"], "a": value})

        paragraph_entry = paragraph(output_data, form_data.get("gender") == "Male")
        output_data["llm_data"] = paragraph_entry
        output_data["llm_prediction"] = (
            paragraph_entry + " " + prediction(input_weight, total_weight)
        )
        output_data["input_weight"] = input_weight
        output_data["total_weight"] = total_weight
        df = pd.DataFrame(output_data)
        df.to_csv(f"data/data_{time.time()}.csv", index=False)

        return result


def merge_survey_data():
    output_filename = "data.csv"
    merged_df = pd.DataFrame()
    for entry in os.scandir("./data"):
        if not entry.name.endswith(".csv"):
            continue

        df = pd.read_csv(entry.path)
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.concat([merged_df, df])

    merged_df.to_csv(f"app/{output_filename}", index=False)
    return output_filename
