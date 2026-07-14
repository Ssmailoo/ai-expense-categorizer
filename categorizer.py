from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

def normalize_amount(amount: str) -> int:
    cleaned = amount.strip().lower()

    if cleaned.endswith("rb"):
        return int(cleaned.replace("rb", "").replace(".", "")) * 1000
    
    return int(cleaned.replace(".", ""))

def categorizer_expense(description, amount):

    contents = f"Description {description}, Amount {amount}"
    config = types.GenerateContentConfig(
        system_instruction = (
            "You are an expense categorization assistant.\n"
            "Categorize each expense into exactly one category.\n\n"

            "Categories:\n"
            "- Food: Daily food and beverages intended for consumption.\n"
            "- Entertainment: Spending for fun, recreation, hobbies, games, movies, or leisure activities.\n"
            "- Self Reward: Spending intended as a personal reward after an achievement, hard work, or a special occasion.\n"
            "- Self Development: Spending for health, fitness, learning, sports, personal care, supplements, vitamins, gym equipment, skincare, and self-improvement. Supplements and vitamins always belong here, even though they are edible.\n"
            "- Other: Anything that does not fit the categories above.\n\n"

            "Confidence Rules:\n"
            "- Return 'high' when the description clearly supports one category.\n"
            "- Return 'low' when the description is ambiguous, lacks sufficient context, or could reasonably belong to multiple categories.\n\n"

            "Examples of low confidence:\n"
            "- Food vs Self Development: 'beli buah untuk program diet', 'protein shake'.\n"
            "- Entertainment vs Self Reward: 'nonton bioskop', 'main game' without explaining the purpose.\n"
            "- Insufficient description: 'bayar 50000', 'transfer', 'belanja'.\n\n"

            "If confidence is low, still choose the single most likely category.\n"
            "Never create new categories."
        ),
        response_schema = {
            "type": "OBJECT",
            "properties": {
            "category": {
                "type": "STRING",
                "enum": ["Food", "Entertainment", "Self Reward", "Self Development", "Other"]
                },
            "confidence": {
                "type": "STRING",
                "enum": ["low", "high"]
                },
            },
            "required": ["category", "confidence"]
        },
    )
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=contents, config=config)
    return(response.text)

def process_expense(description: str, amount: str):
    if not description.strip():
        raise ValueError("Enter the correct value.")
    
    normalized_amount = normalize_amount(amount)
    result = categorizer_expense(description, normalized_amount)
    return result, normalized_amount

if __name__ == "__main__":

    print(normalize_amount(" 150rb "))
    print(normalize_amount("170.000"))
    print(normalize_amount("20000"))

    RUN_API_TEST = False

    if RUN_API_TEST:
        test_cases = [
            ("beli buah untuk diet", "20000"),
            ("bayar 50000", "50000"),
            ("nonton bioskop", "50000"),
        ]

        for description, amount in test_cases:
            result, normalized_amount = process_expense(description, amount)
            print(f"{description} ({amount} -> {normalized_amount}) -> {result}")

    try:
        process_expense("", "10000")
    except ValueError as e:
        print(f"Correctly rejected: {e}")

    try:
        process_expense("   ", "10000")
    except ValueError as e:
        print(f"Correctly rejected: {e}")