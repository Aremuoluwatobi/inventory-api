import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def categorize_inventory(description):
    payload = {
        "model": "llama3.1",

        "prompt": f"""
You are an inventory categorizer.

classify the inventory into ONE category only:
Food, Health, Gadget, Transport, Electronics, Shopping, others.

Inventory: {description}

return only the category name.""",

        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    result = response.json()

    category = result.get("response", "").strip()

    return category
