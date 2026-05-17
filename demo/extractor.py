import json
import re

CRM_KEYWORDS = ["bed", "bedroom", "flat", "apartment", "studio",
                "budget", "£", "moving", "move", "relocating",
                "looking for", "need", "searching"]

APPROXIMATE_KEYWORDS = ["around", "maybe", "ish", "flexible", "roughly", "about"]
HARD_LIMIT_KEYWORDS = ["max", "maximum", "up to", "no more than"]

LONDON_AREAS = [
    "Canary Wharf", "Shoreditch", "Hackney", "Stratford",
    "Kensington", "Chelsea", "Camden", "Paddington",
    "Battersea", "Richmond", "Greenwich", "Canning Town",
    "Isle of Dogs", "King's Cross", "London Bridge",
    "Brixton", "Peckham", "Islington", "Bethnal Green"]

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sept", "oct", "nov", "dec"
]

MONTH_MAP = {
    "jan": "January", "feb": "February", "mar": "March", "apr": "April",
    "may": "May", "jun": "June", "jul": "July", "aug": "August",
    "sept": "September", "oct": "October", "nov": "November", "dec": "December",
    "january": "January", "february": "February", "march": "March", "april": "April",
    "june": "June", "july": "July", "august": "August", "september": "September",
    "october": "October", "november": "November", "december": "December"
}

PET_KEYWORDS = ["pet", "dog", "cat", "animal"]

def is_crm_worthy(message):
    message_lower = message.lower()
    for keyword in CRM_KEYWORDS:
        if keyword in message_lower:
            return True
    return False

def extract_budget(message):
    message_lower = message.lower()

    match = re.search(r'£([\d,]+)', message)

    if not match:
        k_match = re.search(r'(\d+\.?\d*)k', message_lower)
        if k_match:
            value = float(k_match.group(1)) * 1000
            return {"value": int(value), "confidence": "approximate"}

    if not match:
        ish_match = re.search(r'(\d+)\s*ish', message_lower)
        if ish_match:
            return {"value": int(ish_match.group(1)), "confidence": "approximate"}

    if not match:
        return {"value": None, "confidence": "unknown"}

    value = int(match.group(1).replace(",", ""))

    for word in HARD_LIMIT_KEYWORDS:
        if word in message_lower:
            return {"value": value, "confidence": "hard_limit"}

    for word in APPROXIMATE_KEYWORDS:
        if word in message_lower:
            return {"value": value, "confidence": "approximate"}

    return {"value": value, "confidence": "exact"}

def extract_bedrooms(message):
    message_lower = message.lower()

    if "studio" in message_lower:
        return {"value": "studio", "confidence": "exact"}

    match = re.search(r'(\d+)\s*bed', message_lower)

    if match:
        return {"value": int(match.group(1)), "confidence": "exact"}

    return {"value": None, "confidence": "unknown"}

def extract_area(message):
    message_lower = message.lower()
    found_areas = []

    for area in LONDON_AREAS:
        if area.lower() in message_lower:
            found_areas.append(area)

    if len(found_areas) == 0:
        return {"value": None, "confidence": "unknown"}
    elif len(found_areas) == 1:
        return {"value": found_areas[0], "confidence": "exact"}
    else:
        return {"value": found_areas, "confidence": "flexible"}

def extract_move_date(message):
    message_lower = message.lower()
    found_months = []

    for month in MONTHS:
        if re.search(r'\b' + month + r'\b', message_lower):
            if month not in found_months:
                found_months.append(month)

    normalize = lambda m: MONTH_MAP.get(m, m)

    if len(found_months) == 0:
        if "asap" in message_lower or "next month" in message_lower:
            return {"value": "ASAP", "confidence": "approximate"}
        return {"value": None, "confidence": "unknown"}

    if "maybe" in message_lower or "/" in message_lower:
        return {"value": [normalize(m) for m in found_months], "confidence": "approximate"}

    return {"value": normalize(found_months[0]), "confidence": "exact"}

def extract_pet_friendly(message):
    message_lower = message.lower()

    if "no pet" in message_lower:
        return {"value": False, "confidence": "exact"}

    for keyword in PET_KEYWORDS:
        if keyword in message_lower:
            return {"value": True, "confidence": "exact"}

    return {"value": None, "confidence": "unknown"}

def extract_furnished(message):
    message_lower = message.lower()

    if "unfurnished" in message_lower:
        return {"value": False, "confidence": "exact"}

    if "furnished preferred" in message_lower or "furnished ideally" in message_lower:
        return {"value": True, "confidence": "approximate"}

    if "furnished" in message_lower:
        return {"value": True, "confidence": "exact"}

    return {"value": None, "confidence": "unknown"}

def extract(message):
    if not is_crm_worthy(message):
        return {"crm_worthy": False}

    fields = {
        "budget": extract_budget(message),
        "bedrooms": extract_bedrooms(message),
        "area": extract_area(message),
        "move_date": extract_move_date(message),
        "pet_friendly": extract_pet_friendly(message),
        "furnished": extract_furnished(message)
    }

    missing = [key for key, val in fields.items() if val["value"] is None]

    follow_up_map = {
        "budget": "Could you share your approximate budget?",
        "bedrooms": "How many bedrooms are you looking for?",
        "area": "Do you have a preferred area in London?",
        "move_date": "When are you looking to move in?",
        "pet_friendly": "Do you have any pets?",
        "furnished": "Would you prefer a furnished or unfurnished property?"
    }

    follow_up = [follow_up_map[key] for key in missing]

    return {
        "crm_worthy": True,
        "fields": fields,
        "missing_fields": missing,
        "suggested_follow_up": follow_up
    }

if __name__ == "__main__":
    test_messages = [
        "Hi, I'm moving to London in September, budget is around £1800, need 2 bedrooms near Canary Wharf, pet friendly ideally.",
        "Looking for a flat, budget flexible around £1500-1700, somewhere in Zone 2, ASAP.",
        "Hi! Need a 1 bed in Shoreditch, moving next month.",
        "Hi!!! moving asap maybe sept/oct, budget maybe 1700ish but can stretch, relocating with my partner and small dog",
        "Good morning, I am looking for a furnished 2 bedroom flat in Canary Wharf. Budget maximum £2,000. Moving in October. No pets.",
        "Thanks, Saturday viewing works for me!"
    ]

    for i, msg in enumerate(test_messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"Input: {msg[:60]}...")
        print(f"Output:")
        print(json.dumps(extract(msg), indent=2))