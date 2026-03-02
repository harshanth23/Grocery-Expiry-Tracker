import re
from datetime import datetime

def normalize_date(date_str: str) -> str:
    """
    Convert various date formats to dd/mm/yyyy format.
    Handles: 16/01/2021, 16-01-2021, 16 JAN 2021, July 2025, Jan 2026, 2021-01-16, etc.
    For month-only dates (July 2025), returns 01/07/2025
    """
    if not date_str:
        return None
    
    date_str = date_str.strip()
    date_str = re.sub(r"([a-zA-Z])([0-9])", r"\1 \2", date_str)
    date_str = re.sub(r"\s+", " ", date_str)
    
    # Month names mapping
    months = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3, 'ar': 3,
        'apr': 4, 'april': 4, 'ap': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'sept': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }
    
    # Pattern 1: Month name + Year (e.g., "July 2025", "Jan 2026", "APR.2024", "APR2024")
    match = re.match(r'(\w+)\.?\s*(\d{4})', date_str, re.IGNORECASE)
    if match:
        month_name = match.group(1).lower()[:3]  # Get first 3 letters
        year = match.group(2)
        month = months.get(month_name)
        if month:
            return f"01/{month:02d}/{year}"
    
    # Pattern 2: Day Month Year (e.g., "21 Jan 2025" or "16 JAN 2021")
    match = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{2,4})', date_str, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_name = match.group(2).lower()[:3]
        year = match.group(3)
        month = months.get(month_name)
        if month:
            # Handle 2-digit years
            if len(year) == 2:
                year = "20" + year
            return f"{day:02d}/{month:02d}/{year}"
    
    # Pattern 3: DD/MM/YYYY or DD-MM-YYYY (already in correct format or close)
    match = re.match(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', date_str)
    if match:
        day, month, year = match.group(1), match.group(2), match.group(3)
        return f"{int(day):02d}/{int(month):02d}/{year}"
    
    # Pattern 4: YYYY-MM-DD
    match = re.match(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', date_str)
    if match:
        year, month, day = match.group(1), match.group(2), match.group(3)
        return f"{int(day):02d}/{int(month):02d}/{year}"
    
    # Pattern 5: DD/MM/YY or DD-MM-YY
    match = re.match(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})$', date_str)
    if match:
        day, month, year = match.group(1), match.group(2), match.group(3)
        year = "20" + year  # Assume 20xx
        return f"{int(day):02d}/{int(month):02d}/{year}"
    
    # If no pattern matches, return as is
    return date_str


def extract_label_info(text: str) -> dict:
    """
    Extract expiry date, PKD/MFG date, and batch number from OCR text.
    All dates are normalized to dd/mm/yyyy format.
    """

    # More comprehensive date pattern to match various formats
    date_pattern = (
        r"(?:\d{2}[/-]\d{2}[/-]\d{4})|"  # 16/01/2021 or 16-01-2021
        r"(?:\d{1,2}\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s*\d{2,4})|"  # 16 JAN 2021, 16JAN21, 16 JAN.2021
        r"(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s*\d{4})|"  # July 2025, Jan 2026, APR.2024
        r"(?:[a-z]{2,4}\.?\s*\d{4})|"  # OCR-short months like AR2026
        r"(?:\d{4}[/-]\d{2}[/-]\d{2})|"  # 2021-01-16
        r"(?:\d{1,2}[/-]\d{1,2}[/-]\d{2})"  # 16/01/21 or 16-01-21
    )

    # Expiry date patterns - includes "Ex.Date" format
    expiry = re.search(
        rf"(exp\.?|expiry|ex\.?\s*date|ex\.?|best\s*before|use\s*by|e\s*/?\s*d\s*t|e\s*dt|edt)\s*(?:date|of)?\s*[:.-]*\s*({date_pattern})",
        text,
        flags=re.IGNORECASE
    )

    # MFG date patterns - includes "DL of mfg" format and "Dt. of mfg" format
    mfg = re.search(
        rf"(mfg\.?|manufactured|pkd\.?|packed|pack\s*date|date\s*of\s*manufacturing|dom|dl\s*of\s*mfg|dl\s+mfg|dt\.?\s*of\s*mfg|dt\.?\s+mfg|m\s*/?\s*d\s*t|m\s*dt|mdt|/\s*dt|\bdt\b)\s*(?:date|of)?\s*[:.-]*\s*({date_pattern})",
        text,
        flags=re.IGNORECASE
    )

    batch = re.search(
        r"(batch|lot|bn|b\.?\s*no|b\.?\s*n0|batch\s*no)[^a-z0-9]*([a-z0-9-]+)",
        text,
        flags=re.IGNORECASE
    )

    return {
        "expiry_date": normalize_date(expiry.group(2)) if expiry else None,
        "mfg_date": normalize_date(mfg.group(2)) if mfg else None,
        "batch_no": batch.group(2) if batch else None
    }
