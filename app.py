from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

from ocr_engine import extract_text
from item_name_extractor import extract_item_name_from_product
from regex_utils import extract_label_info

app = Flask(__name__)

TEMP_DIR = "temp_images"
SAVED_ITEMS_FILE = "saved_items.json"
os.makedirs(TEMP_DIR, exist_ok=True)

ALLOWED_TYPES = {"Grocery", "Fruit", "Vegetable", "Medicine"}

def load_saved_items():
    if os.path.exists(SAVED_ITEMS_FILE):
        with open(SAVED_ITEMS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(SAVED_ITEMS_FILE, 'w') as f:
        json.dump(items, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan-item", methods=["POST"])
def scan_item():
    item_type = request.form.get("item_type")

    if item_type not in ALLOWED_TYPES:
        return jsonify({"error": "Invalid item type"}), 400

    product_img = request.files["product_image"]
    label_img = request.files["label_image"]

    product_path = os.path.join(TEMP_DIR, "product.jpg")
    label_path = os.path.join(TEMP_DIR, "label.jpg")

    product_img.save(product_path)
    label_img.save(label_path)

    # 🔹 FRUIT / VEGETABLE FLOW (Image Classification + Rule Expiry)
    if item_type in ["Fruit", "Vegetable"]:

        item_name = classify_fruit(product_path)
        expiry_days = estimate_expiry_days(item_name)
        expiry_date = get_expiry_date(expiry_days)

        print("FRUIT/VEG CLASSIFIED:")
        print(item_name)
        print("Estimated Days:", expiry_days)
        print("=" * 50)

        return jsonify({
            "item_type": item_type,
            "item_name": item_name,
            "mfg": "Not Applicable",
            "exp": expiry_date,
            "estimated_days_remaining": expiry_days
        })

    # 🔹 GROCERY / MEDICINE FLOW (Existing OCR Logic)
    else:
        item_name = extract_item_name_from_product(product_path, item_type)
        print("EXTRACTED PRODUCT NAME:")
        print(item_name)
        print("=" * 50)

        text = extract_text(label_path)
        print("=" * 50)
        print("OCR EXTRACTED TEXT FROM LABEL:")
        print(text)
        print("=" * 50)
        
        label_data = extract_label_info(text)
        
        print("EXTRACTED LABEL DATA:")
        print(label_data)
        print("=" * 50)

        return jsonify({
            "item_type": item_type,
            "item_name": item_name or "Unknown Item",
            "mfg": label_data["mfg_date"] or "Not detected",
            "exp": label_data["expiry_date"] or "Not detected"
        })


@app.route("/save-item", methods=["POST"])
def save_item():
    data = request.get_json()
    
    items = load_saved_items()
    
    new_item = {
        "id": len(items) + 1,
        "item_type": data.get("item_type"),
        "item_name": data.get("item_name"),
        "mfg": data.get("mfg"),
        "exp": data.get("exp"),
        "quantity": data.get("quantity", 1),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    items.append(new_item)
    save_items(items)
    
    return jsonify({"success": True, "message": "Item saved successfully!"})


@app.route("/get-items", methods=["GET"])
def get_items():
    items = load_saved_items()
    return jsonify(items)


if __name__ == "__main__":
    app.run(debug=True)
