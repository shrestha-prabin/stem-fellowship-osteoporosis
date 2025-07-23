import random

import pandas as pd
from flask import Flask, render_template, request, send_file
from transformers import pipeline

from generate_data import generate_llm_data
from preprocess import process_text
from summarization import generate_summary, generate_summary_deepseek
from utils import export_form_data, merge_survey_data


def label_to_prediction(label):
    print(label)
    if label == "LABEL_0":
        category = "low"
    else:
        category = "high"

    return f"The patient has {category} risk of osteoporosis."


def label_to_percentage(label):
    print(label)
    if label == "LABEL_0":
        percentage = random.randint(7, 10)
    elif label == "LABEL_1":
        percentage = random.randint(15, 20)
    else:
        percentage = random.randint(34, 40)

    return f"The patient is at {percentage}% risk of osteoporosis."


roberta_pipe = pipeline(
    "text-classification", model="aaslan47/robota-sequence-classifier"
)

distilbert_pipe = pipeline(
    "text-classification", model="aaslan47/distilbert-sequence-classifier"
)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/result", methods=["POST"])
    def result():
        details, output_data = export_form_data(request.form)

        # Convert form data to paragraph
        data = generate_llm_data(request.form)

        # Preprocess text
        data = process_text(data)

        result1 = roberta_pipe(data)
        result2 = distilbert_pipe(data)

        print(result1, result2)

        return render_template(
            "result2.html",
            result=details,
            # roberta_result=label_to_percentage(result1[0]["label"]),
            # distilbert_result=label_to_percentage(result2[0]["label"]),
            roberta_result=label_to_prediction(result1[0]["label"]),
            distilbert_result=label_to_prediction(result2[0]["label"]),
            # llama_result=generate_summary(
            #     "meta-llama/Llama-3.1-8B-Instruct",
            #     "fireworks-ai",
            #     output_data["llm_data"],
            # ),
            deepseek_result=generate_summary_deepseek(output_data["llm_data"]),
        )

    @app.route("/download")
    def download():
        filename = merge_survey_data()
        return send_file(filename, as_attachment=True)

    return app
