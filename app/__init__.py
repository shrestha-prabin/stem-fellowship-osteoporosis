import pandas as pd
from flask import Flask, render_template, request, send_file
from transformers import pipeline

from utils import export_form_data, merge_survey_data

label_to_prediction = {
    "LABEL_1": "low",
    "LABEL_2": "medium",
    "LABEL_3": "high",
}

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
        # details = export_form_data(request.form)
        # return render_template("result.html", result=details)

        details, output_data = export_form_data(request.form)

        data = [output_data["llm_data"]]

        result1 = roberta_pipe(data)
        result2 = distilbert_pipe(data)

        return render_template(
            "result2.html",
            result=details,
            roberta_result=label_to_prediction[result1[0]["label"]],
            distilbert_result=label_to_prediction[result2[0]["label"]],
        )

    @app.route("/download")
    def download():
        filename = merge_survey_data()
        return send_file(filename, as_attachment=True)

    return app
