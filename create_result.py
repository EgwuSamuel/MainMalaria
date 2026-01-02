import os
from flask import render_template, url_for


def make(filename: str, label: str, confidence: float):
    image_url = url_for("static", filename=f"uploads/{os.path.basename(filename)}")
    return render_template(
        "result.html",
        image_url=image_url,
        label=label,
        confidence=round(float(confidence), 2),
    )
