from paddleocr import PaddleOCR

# Load once (heavy model)
ocr = PaddleOCR(use_angle_cls=True, lang="en")

def extract_text(image_path: str) -> str:
    """
    Extracts all readable text from a label image using PaddleOCR.
    """
    result = ocr.ocr(image_path, cls=True)

    texts = []
    for block in result:
        for line in block:
            texts.append(line[1][0])

    return " ".join(texts).lower()
