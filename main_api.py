from fastapi import FastAPI, HTTPException
from database import get_all_expenses, save_expense, get_total_by_category, delete_expense
from pydantic import BaseModel
from categorizer import process_expense

app = FastAPI()

class Expense(BaseModel):
    id: int
    description: str
    amount: int
    category: str
    confidence: str
    created_at: str

class ExpenseInput(BaseModel):
    description: str
    amount: str


@app.get("/expenses")
def list_expenses():
    rows = get_all_expenses()

    result = []
    for row in rows:
        expense = Expense(
            id=row[0],
            description=row[1],
            amount=row[2],
            category=row[3],
            confidence=row[4],
            created_at=row[5],
        )

        result.append(expense)
    return result


@app.post("/expenses")
def create_expense(data: ExpenseInput):
    try:
        result, normalized_amount = process_expense(data.description, data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    save_expense(
        description=data.description,
        amount=normalized_amount,
        category=result["category"],
        confidence=result["confidence"],
    )

    return {
        "message": "Expense Saved",
        "category": result["category"],
        "confidence": result["confidence"],
    }


@app.get("/expenses/total/{category}")
def get_category_total(category: str):
    return {"category": category, "total": get_total_by_category(category)}


@app.delete("/expenses/{id}")
def deleted_expense(id: int):
    delete_expense(id)
    return {
        "message": f"this expense {id} success deleted"
    }