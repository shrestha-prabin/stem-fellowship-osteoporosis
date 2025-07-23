import json

with open("app/static/data.json", "r") as f:
    form_meta = json.load(f)


def generate_llm_data(form_data):

    data = {}

    for form_item in form_meta:
        col = form_item["name"]
        if form_item.get("type") == "multiselect":
            selected_values = form_data.getlist(col)
            value = ", ".join(selected_values)
        else:
            value = form_data.get(col)
        data[col] = value

    is_male = data.get("gender") == "Male"

    data_format = {
        "gender": f"The patient is {data['gender']}",
        "hipFracture": f"The patient has reported a history of hip fracture {data['hipFracture']}",
        "spineFracture": f"Spine fracture {data['spineFracture']}",
        "otherAdultFracture": f"And other adult fractures {data['otherAdultFracture']}",
        "fractureAge": f"With the fracture occurring at the age of {data['fractureAge']}",
        "fracturedBones": f"The specific bone that was fractured was the {data['fracturedBones']}",
        "priorDexaScan": f"A DEXA scan has previously been performed {data['priorDexaScan']}",
        "lastDexaScanDetails": f"With the most recent scan details noted as {data['lastDexaScanDetails']}",
        "fragilityFractureAfter45": f"The patient has experienced a fragility fracture after age 45 {data['fragilityFractureAfter45']}",
        "youngLowTraumaFracture": f"And a low-trauma fracture at a younger age {data['youngLowTraumaFracture']}",
        "currentlyInMenopause": f"The patient is currently in menopause {data['currentlyInMenopause']}",
        "ageAtMenopause": f"Which began at the age of {data['ageAtMenopause']}",
        "menopauseType": f"And is classified as {data['menopauseType']} menopause",
        "menopauseStatus": f"The patient had been through menopause {data['menopauseStatus']}",
        "menopausalStage": f"The patient is at {data['menopausalStage']} stage.",
        "premenopausalAmenorrhea": f"The patient had  premenopausal Amenorrhea {data.get('premenopausalAmenorrhea')}",
        "parentHipFracture": f"They have parent hip fracture {data['parentHipFracture']}",
        "delayedPuberty": f"They had delayed puberty {data['delayedPuberty']}",
        "familyHistoryOsteoporosis": f"There is a family history of osteoporosis {data['familyHistoryOsteoporosis']}",
        "ovariesRemoved": f"The ovaries have been removed {data['ovariesRemoved']}",
        "familyHistoryHipFracture": f"And a parental history of hip fracture {data['familyHistoryHipFracture']}",
        "currentSmoker": f"The patient's smoking status is currently {data['currentSmoker']}",
        "everSmoked": f"With a history of smoking described as {data['everSmoked']}",
        "excessiveAlcoholIntake": f"Alcohol intake is noted as excessive: {data['excessiveAlcoholIntake']}",
        "historyOfFalls": f"There is a history of falls {data['historyOfFalls']}",
        "eatingDisorder": f"The patient also has a history of eating disorder {data['eatingDisorder']}",
        "highCalciumDiet": f"Nutritional intake includes a high-calcium diet {data['highCalciumDiet']}",
        "calciumSupplements": f"Along with the use of calcium supplements {data['calciumSupplements']}",
        "vitaminDSupplements": f"And vitamin D supplements {data['vitaminDSupplements']}",
        "longTermSteroids": f"The patient has a history of long-term steroid use {data['longTermSteroids']}",
        "takenEstrogen": f"Estrogen therapy {data['takenEstrogen']}",
        "glucocorticoidUse": f"They have taken glucocorticoid {data['glucocorticoidUse']}",
        "hormoneTherapy": f"They have taken hormon therapy {data['hormoneTherapy']}",
        "osteoporosisMedications": f"And has taken osteoporosis medications {data['osteoporosisMedications']}",
        "ssriUse": f"The SSRI usage for the patient is {data['ssriUse']}",
        "ppiUse": f"And PPI usage is {data['ppiUse']}",
        "rheumatoidArthritis": f"Relevant medical conditions include rheumatoid arthritis {data['rheumatoidArthritis']}",
        "primaryHyperparathyroidism": f"Primary Hyperthyroidism {data['primaryHyperparathyroidism']}",
        "hyperthyroidism": f"Hyperthyroidism {data['hyperthyroidism']}",
        "crohnsOrCeliac": f"Crohn’s or celiac disease {data['crohnsOrCeliac']}",
        "kidneyDiseaseOrDialysis": f"Kidney disease or dialysis {data['kidneyDiseaseOrDialysis']}",
        "copd": f"COPD {data['copd']}",
        "hivAids": f"HIV/AIDS {data['hivAids']}",
        "depression": f"Depression {data['depression']}",
        "diabetes": f"And diabetes {data['diabetes']}",
        "recentWeightLoss": f"The patient has recently experienced weight loss {data['recentWeightLoss']}",
        "recentHeightLoss": f"And height loss {data['recentHeightLoss']}",
        "spineSurgery": f"And has undergone spine surgery {data['spineSurgery']}",
        "hipSurgery": f"Or hip surgery {data['hipSurgery']}",
        "gastricSurgery": f"Or gastric surgery {data['gastricSurgery']}",
        "currentlyPregnant": f"Lastly, it is noted whether the patient is currently pregnant {data['currentlyPregnant']}",
    }

    llm_data = ""

    for item in form_meta:
        if is_male and item.get("femaleOnly"):
            continue
        llm_data += data_format[item["name"]] + ". "

    return llm_data
