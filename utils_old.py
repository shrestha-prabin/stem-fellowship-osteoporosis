import json
import os
import time

import pandas as pd


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
