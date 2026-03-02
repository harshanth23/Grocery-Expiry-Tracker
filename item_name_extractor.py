import math
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def box_area(box):
    # Approximate rectangle area
    width = math.dist(box[0], box[1])
    height = math.dist(box[1], box[2])
    return width * height


def extract_item_name_from_product(image_path, item_type=None):
    """
    Extracts the most likely product name from product image.
    For medicines, prefers text with medical keywords (IP, mg, Tablets, etc.)
    For other products, tries to skip brand names and get the actual product name.
    """
    result = ocr.ocr(image_path, cls=True)

    candidates = []

    # Medical/pharmaceutical keywords that indicate a product name
    medical_keywords = ['ip', 'mg', 'ml', 'gm', 'tablet', 'capsule', 'syrup', 
                       'suspension', 'injection', 'ointment', 'cream', 'drops']

    for block in result:
        for line in block:
            box = line[0]
            text = line[1][0]
            conf = line[1][1]

            area = box_area(box)
            y_position = box[0][1]  # Top Y coordinate

            # Filter by confidence
            if conf > 0.5:
                text_lower = text.lower()
                has_medical_keyword = any(keyword in text_lower for keyword in medical_keywords)
                candidates.append({
                    'text': text.strip(),
                    'area': area,
                    'y_pos': y_position,
                    'conf': conf,
                    'is_medical': has_medical_keyword
                })

    # Debug: Print all detected candidates with area
    print("ALL OCR CANDIDATES (sorted by area):")
    for c in sorted(candidates, key=lambda x: x['area'], reverse=True):
        print(f"Text: '{c['text']}', Area: {c['area']:.2f}, Y: {c['y_pos']:.2f}, Conf: {c['conf']:.2f}")
    print("=" * 50)

    if not candidates:
        return "Unknown"

    # Sort by area descending to get largest texts
    candidates.sort(key=lambda x: x['area'], reverse=True)

    # Define a threshold: big texts are those >= 15% of the largest area
    largest_area = candidates[0]['area']
    min_area_threshold = largest_area * 0.15
    big_texts = [c for c in candidates if c['area'] >= min_area_threshold]

    # Use medicine-specific logic only if item_type is 'Medicine'
    if item_type and item_type.lower() == 'medicine':
        medical_big_texts = [c for c in big_texts if c['is_medical']]
        if len(medical_big_texts) >= 1:
            return medical_big_texts[0]['text']
    # Otherwise, pick the largest big text
    if len(big_texts) >= 1:
        return big_texts[0]['text']
    else:
        return candidates[0]['text']
