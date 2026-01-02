import os
from typing import Tuple

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import preprocessing
import PIL.Image

_model = None
CLASS_NAMES = ["Parasitized", "Uninfected"]
MODEL_PATH = os.path.join("models", "malaria_model_94")


def _load_model():
    global _model
    if _model is None:
        _model = keras.models.load_model(MODEL_PATH)
    return _model


def _prepare_image(path: str, img_height: int = 150, img_width: int = 150):
    img = preprocessing.image.load_img(path, target_size=(img_height, img_width))
    img_array = preprocessing.image.img_to_array(img)
    return tf.expand_dims(img_array, 0)


def predict_image(path: str, img_height: int = 150, img_width: int = 150) -> Tuple[str, float]:
    model = _load_model()
    img_batch = _prepare_image(path, img_height=img_height, img_width=img_width)

    predictions = model.predict(img_batch)
    score = tf.nn.softmax(predictions[0])
    confidence = float(100 * np.max(score))
    label = CLASS_NAMES[int(np.argmax(score))]
    return label, confidence


def resize_image(path: str, new_width: int = 150, new_height: int = 150):
    with PIL.Image.open(path) as im:
        if im.size != (new_width, new_height):
            resized = im.resize((new_width, new_height))
            resized.save(path)


def predict(path: str) -> Tuple[str, float]:
    resize_image(path)
    return predict_image(path)


if __name__ == "__main__":
    print(predict_image("parasite.png"))
