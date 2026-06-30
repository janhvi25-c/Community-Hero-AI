def analyze_report(title, location, description):

    text = (title + " " + description).lower()

    if "accident" in text or "crash" in text or "collision" in text:
        return """Category: Accident
Priority: Highest"""

    elif "garbage" in text or "waste" in text or "dustbin" in text:
        return """Category: Garbage
Priority: Medium"""

    elif "pothole" in text or "road damage" in text or "crack" in text:
        return """Category: Road Damage
Priority: High"""

    elif "water" in text or "leakage" in text or "pipe" in text:
        return """Category: Water Leakage
Priority: Medium"""

    elif "street light" in text or "streetlight" in text or "lamp" in text or "light not working" in text:
        return """Category: Street Light
Priority: Low"""

    else:
        return """Category: Other
Priority: Low"""