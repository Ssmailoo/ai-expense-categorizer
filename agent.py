from dotenv import load_dotenv
from google.genai import types
from google import genai
from database import save_expense, get_all_expenses, get_total_by_category, delete_expense
from categorizer import categorizer_expense


load_dotenv()
client = genai.Client()

def describe_tools() -> list[dict]:
    """
    Return tool schema that Gemini API can understand,
    Each tool needs: name, description, and parameters,
    """
    tools = [
        {
            "name": "get_total_by_category",
            "description": "Return the total amount of expenses for a given category from the expense database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The expense category, such as Food, Entertainment, Self Development, or Self Reward."
                    }
                },
                "required": ["category"]
            }
        },
        {
            "name": "save_expense",
            "description": "Save a new expense record with its description and amount into the database. The category and confidence level will be determined automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A short description of the expense."
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount of money spent."
                    }
                },
                "required": [
                    "description",
                    "amount"
                ]
            }
        },
        {
            "name": "get_all_expenses",
            "description": "Returns all saved expense records from the expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "delete_expense",
            "description": "Delete an expense record from the expense database by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "The unique ID of the expense to delete."
                    }
                },
                "required": ["id"]
            }
        }
    ]
    return tools


def build_tools():
    function_declarations = [
        types.FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters_json_schema=tool["parameters"]
        )
        for tool in describe_tools()
    ]
    return [types.Tool(function_declarations=function_declarations)]

tool_map = {
    "save_expense": save_expense,
    "get_all_expenses": get_all_expenses,
    "get_total_by_category": get_total_by_category,
    "delete_expense": delete_expense,
}

def run_agent(user_message: str) -> str:
    """
    Runs the agent loop: sends user message to gemini,
    ececutes tool calls until gemini returns a final text answer.
    """
    conversation = [user_message]
    config = types.GenerateContentConfig(tools=build_tools())

    while True:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=conversation,
            config=config
        )
        part = response.candidates[0].content.parts[0]

        if part.function_call:
            tool_name = part.function_call.name
            tool_args = part.function_call.args

            print(f"[DEBUG] Gemini memanggil tool: {tool_name} dengan args: {dict(tool_args)}")

            if tool_name == "save_expense":
                categorization = categorizer_expense(tool_args["description"], tool_args["amount"])
                tool_args["category"] = categorization["category"]
                tool_args["confidence"] = categorization["confidence"]

            result = tool_map[tool_name](**tool_args)

            conversation.append(part)
            conversation.append({
                "function_response": {
                    "name": tool_name,
                    "response": {"result": result}
                }
            })

            continue

        else:
            return part.text
        
print(run_agent("tampilkan semua pengeluaran saya, lalu kasih tahu juga total kategori makanan"))
print(run_agent("hapus pengeluaran nasi padang yang tadi saya catat"))