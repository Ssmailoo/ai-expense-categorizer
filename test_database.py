import pytest
from database import init_db, save_expense, get_all_expenses, get_total_by_category, delete_expense

@pytest.fixture
def test_db_path(tmp_path):
    db_path = str(tmp_path / "test_expenses.db")
    init_db(db_path)
    yield db_path

def test_save_expense_then_get_all_expenses_returns_it(test_db_path):
    save_expense(
        description="test lunch",
        amount=15000,
        category="Food",
        confidence="high",
        db_path=test_db_path
    )

    expenses = get_all_expenses(db_path=test_db_path)

    assert len(expenses) == 1

def test_get_total_by_category_sums_matching_expenses(test_db_path):
    save_expense(description="lunch", amount=15000, category="Food", confidence="high", db_path=test_db_path)
    save_expense(description="dinner", amount=20000, category="Food", confidence="high", db_path=test_db_path)
    save_expense(description="movie", amount=50000, category="Entertainment", confidence="high", db_path=test_db_path)

    total_food = get_total_by_category("Food", db_path=test_db_path)

    assert total_food == 35000

def test_get_total_by_category_returns_zero_when_no_matching_expenses(test_db_path):
    total = get_total_by_category("Food", db_path=test_db_path)

    assert total == 0

def test_delete_expense_removes_it_from_database(test_db_path):
    save_expense(description="temporary item", amount=1000, category="Food", confidence="high", db_path=test_db_path)
    expense_before= get_all_expenses(db_path=test_db_path)
    expense_id = expense_before[0][0]

    delete_expense(id=expense_id, db_path=test_db_path)

    expenses_after = get_all_expenses(db_path=test_db_path)
    assert len(expenses_after) == 0