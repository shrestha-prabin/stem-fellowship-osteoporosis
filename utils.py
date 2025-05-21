import json
import os
import time

import pandas as pd
def paragraph(data: dict) -> str:
    formatted_paragraph = f"""
    The patient has reported a history of hip fracture {data['hipFracture'][0]}, spine fracture {data['spineFracture'][0]}, and other adult fractures {data['otherAdultFracture'][0]}, with the fracture occurring at the age of {data['fractureAge'][0]}. The specific bone that was fractured was the {data['fracturedBones'][0]}. A DEXA scan has previously been performed {data['priorDexaScan'][0]}, with the most recent scan details noted as {data['lastDexaScanDetails'][0]}. The patient has experienced a fragility fracture after age 45 {data['fragilityFractureAfter45'][0]} and a low-trauma fracture at a younger age {data['youngLowTraumaFracture'][0]}. In terms of reproductive history, the patient is currently in menopause {data['currentlyInMenopause'][0]}, which began at the age of {data['ageAtMenopause'][0]}, and is classified as {data['menopauseType'][0]} menopause. The ovaries have been removed {data['ovariesRemoved'][0]}. There is a family history of osteoporosis {data['familyHistoryOsteoporosis'][0]} and a parental history of hip fracture {data['familyHistoryHipFracture'][0]}. The patient's smoking status is currently {data['currentSmoker'][0]}, with a history of smoking described as {data['everSmoked'][0]}. Alcohol intake is noted as excessive: {data['excessiveAlcoholIntake'][0]}, and there is a history of falls {data['historyOfFalls'][0]}. The patient also has a history of {data['eatingDisorder'][0]}. Nutritional intake includes a high-calcium diet {data['highCalciumDiet'][0]}, along with the use of calcium supplements {data['calciumSupplements'][0]} and vitamin D supplements {data['vitaminDSupplements'][0]}. Medically, the patient has a history of long-term steroid use {data['longTermSteroids'][0]}, estrogen therapy {data['takenEstrogen'][0]}, and has taken osteoporosis medications {data['osteoporosisMedications'][0]}. The SSRI usage for the patient is {data['ssriUse'][0]} and PPI usage is {data['ppiUse'][0]}. Relevant medical conditions include rheumatoid arthritis {data['rheumatoidArthritis'][0]}, hyperthyroidism {data['hyperthyroidism'][0]}, Crohn’s or celiac disease {data['crohnsOrCeliac'][0]}, kidney disease or dialysis {data['kidneyDiseaseOrDialysis'][0]}, COPD {data['copd'][0]}, HIV/AIDS {data['hivAids'][0]}, depression {data['depression'][0]}, and diabetes {data['diabetes'][0]}. The patient has recently experienced weight loss {data['recentWeightLoss'][0]} and height loss {data['recentHeightLoss'][0]}, and has undergone spine surgery {data['spineSurgery'][0]} or hip surgery {data['hipSurgery'][0]} or gastric surgery {data['gastricSurgery'][0]}. Lastly, it is noted whether the patient is currently pregnant {data['currentlyPregnant'][0]}.
"""

    return formatted_paragraph

def export_form_data(form_data):
    result = []
    with open("./app/static/data.json", encoding="utf-8") as f:
        form_meta = json.load(f)

        output_data = {}
        for form_item in form_meta:
            col = form_item["name"]
            if form_item.get("type") == "multiselect":
                selected_values = form_data.getlist(col)
                value = ", ".join(selected_values)
            else:
                value = form_data.get(col)

            print(col, value)
            output_data[col] = [value]
            result.append({"q": form_item["question"], "a": value})
        paragraph_entry = paragraph(output_data)
        output_data['llm_data'] = paragraph_entry
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
