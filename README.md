# AI Expense Categorizer

A REST API that automatically categorizes personal expenses using AI (Google Gemini), with persistent storage in SQLite.

You send a raw expense description (e.g. "beli kopi di indomaret") and an amount (e.g. "20rb"), and the system normalizes the amount, classifies it into a category with a confidence level, and stores the result — accessible via a full HTTP API.

## Features

**AI-powered categorization**
classifies expenses into 5 categories (Food, Entertainment, Self Reward, Self Development, Other) using Google Gemini with structured output.
**Confidence scoring**
flags ambiguous descriptions as `low` confidence instead of guessing silently.
**Amount normalization**
parses informal Indonesian number formats (`"150rb"`, `"20.000"`) into clean integers.
**Persistent storage**
all expenses saved to SQLite, with parameterized queries throughout (SQL-injection safe).
**REST API**
full CRUD-style access via FastAPI, with auto-generated interactive docs.

## Tech Stack

- **Python 3.14**
- **FastAPI** — web framework / API layer
- **Pydantic** — request/response validation
- **SQLite** (`sqlite3`) — persistence
- **Google Gemini API** (`google-genai`) — expense categorization
- **Uvicorn** — ASGI server

## Project Structure

ai-expense-categorizer/
categorizer.py    # AI logic: normalize_amount, categorize_expense, process_expense
database.py        # SQLite logic: init_db, save_expense, get_all_expenses
get_total_by_category
update_expense
delete_expense
├── main.py             # CLI entry point (terminal input)
├── main_api.py        # FastAPI entry point (HTTP API)
└── README.md

## Setup & Run

1. Clone the repository and navigate into it:
   cd ai-expense-categorizer

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install fastapi uvicorn google-genai python-dotenv

4. Add your Gemini API key to a `.env` file:
   GEMINI_API_KEY=your_api_key_here

5. Run the API server:
   uvicorn main_api:app --reload

6. Open the interactive API docs in your browser:
   http://127.0.0.1:8000/docs

## API Endpoints

### `GET /expenses`
Returns all saved expenses.

**Response:**
[
  {
    "id": 2,
    "description": "makan siang",
    "amount": 25000,
    "category": "Food",
    "confidence": "high",
    "created_at": "2026-07-27 20:16:16"
  }
]
### `POST /expenses`
Categorizes and saves a new expense.

**Request body:**
{
  "description": "makan siang",
  "amount": "25000"
}

**Response:**
{
  "message": "Expense Saved",
  "category": "Food",
  "confidence": "high"
}

### `GET /expenses/total/{category}`
Returns the total amount spent in a given category.

**Example:** `GET /expenses/total/Food`

**Response:**
{
  "category": "Food",
  "total": 25000
}

### `DELETE /expenses/{id}`
Deletes an expense by its ID.

**Example:** `DELETE /expenses/1`
**Response:**
{
  "message": "this expense 1 success deleted"
}

## Notes

- All monetary amounts are stored as integers (IDR, no decimals).
- Category confidence is marked `low` when a description is ambiguous (e.g. "bayar 50000" with no further context) — this is intentional, to avoid silently mislabeling unclear expenses.