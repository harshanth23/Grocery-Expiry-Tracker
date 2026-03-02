import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from datetime import datetime, timedelta

# Load pretrained MobileNetV2 (ImageNet)
model = MobileNetV2(weights="imagenet")

FRUIT_EXPIRY_DAYS = {
    "banana": 3,
    "apple": 7,
    "orange": 10,
    "mango": 4,
    "pineapple": 5,
    "carrot": 7,
    "broccoli": 5,
    "cucumber": 4,
    "tomato": 5,
    "potato": 10,
    "onion": 14
}

def classify_fruit(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    decoded = decode_predictions(preds, top=1)[0][0]

    label = decoded[1].lower()
    return label

def estimate_expiry_days(fruit_name):
    for key in FRUIT_EXPIRY_DAYS:
        if key in fruit_name:
            return FRUIT_EXPIRY_DAYS[key]
    return 5  # default fallback

def get_expiry_date(days):
    expiry_date = datetime.now() + timedelta(days=days)
    return expiry_date.strftime("%d/%m/%Y")