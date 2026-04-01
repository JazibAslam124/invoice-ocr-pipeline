import re
from dateutil import parser as dateparser

def parse_date_safe(date_str: str) -> str:
    try:
        return dateparser.parse(date_str, dayfirst=True).strftime("%Y-%m-%d")
    except:
        return date_str  # return raw if parsing fails

def extract_fields(ocr_lines: list) -> dict:
    full_text = "\n".join([l["text"] for l in ocr_lines])
    lines = [l["text"] for l in ocr_lines]

    result = {
        "vendor": None,
        "invoice_number": None,
        "date": None,
        "due_date": None,
        "subtotal": None,
        "tax": None,
        "total": None,
        "currency": "USD",
        "raw_text": full_text
    }

    # Vendor
    skip_words = {"invoice", "logo", "bill to", "ship to"}
    for line in lines[:8]:
        clean = line.strip()
        if len(clean) > 3 and clean.lower() not in skip_words:
            result["vendor"] = clean
            break

    # Invoice number
    inv = re.search(r'invoice\s*#?\s*[:\-]?\s*([A-Z0-9\-]{3,20})', full_text, re.IGNORECASE)
    if inv:
        result["invoice_number"] = inv.group(1).strip()

    # All date formats covered:
    date_patterns = [
        r'\b(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})\b',       # 11/02/2019, 11.02.2019
        r'\b(\d{4}[/.\-]\d{1,2}[/.\-]\d{1,2})\b',          # 2019-02-11
        r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4})\b',  # 11 Feb 2019
        r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4})\b', # Feb 11, 2019
        r'\b(\d{1,2}\s+\d{1,2}\s+\d{4})\b',                # 11 02 2019
    ]

    dates_found = []
    for pattern in date_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        for m in matches:
            normalized = parse_date_safe(m)
            if normalized not in dates_found:
                dates_found.append(normalized)

    if dates_found:
        result["date"] = dates_found[0]
        if len(dates_found) > 1:
            result["due_date"] = dates_found[-1]

    # Currency
    if any(c in full_text for c in ['$', 'USD']):
        result["currency"] = "USD"
    elif any(c in full_text for c in ['€', 'EUR']):
        result["currency"] = "EUR"
    elif any(c in full_text for c in ['£', 'GBP']):
        result["currency"] = "GBP"

    # Total
    total = re.search(r'\bTOTAL\b[^\d]*\$?\s*(\d{1,6}[.,]\d{2})', full_text, re.IGNORECASE)
    if total:
        result["total"] = float(total.group(1).replace(',', '.'))

    # Subtotal
    subtotal = re.search(r'subtotal[^\d]*(\d{1,6}[.,]\d{2})', full_text, re.IGNORECASE)
    if subtotal:
        result["subtotal"] = float(subtotal.group(1).replace(',', '.'))

    # Tax
    tax = re.search(r'(?:tax|mwst|vat)[^\d]*(\d{1,6}[.,]\d{2})\b', full_text, re.IGNORECASE)
    if tax:
        result["tax"] = float(tax.group(1).replace(',', '.'))

    return result