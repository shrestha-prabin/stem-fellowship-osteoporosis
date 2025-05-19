import pickle

import pandas as pd
from flask import Flask, render_template, request, send_file

from utils import export_form_data, merge_survey_data


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/result", methods=["POST"])
    def result():
        details = export_form_data(request.form)
        return render_template("result.html", result=details)

    @app.route("/download")
    def download():
        filename = merge_survey_data()
        return send_file(filename, as_attachment=True)

    return app
