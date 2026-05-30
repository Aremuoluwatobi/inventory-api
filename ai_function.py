import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def categorize_inventory(description):
    payload = {
        "model": "llama3.1",
        "prompt": f"""
You are an inventory categorizer.

Classify the inventory into ONE category only:
Food, Health, Gadget, Transport, Electronics, Shopping, Others.

Rules:
Return one category with no explanation

Inventory: {description}

Return only the category name.
""",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
