import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import create_result
import malaria_prediction

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def upload_form():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            label, confidence = malaria_prediction.predict(file_path)
            return create_result.make(file_path, label, confidence)

        flash("Allowed image types are -> png, jpg, jpeg")
        return redirect(request.url)

    return render_template("form.html")


@app.route("/result")
def result_page():
    return render_template("result.html", image_url=None, label=None, confidence=None)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename=f"uploads/{filename}"), code=301)


if __name__ == "__main__":
    app.run()
