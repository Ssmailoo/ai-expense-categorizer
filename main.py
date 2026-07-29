from categorizer import process_expense
from database import init_db, save_expense
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    init_db()

    amount = input("amount: ")
    description = input("description: ")

    try:
        result, normalized_amount = process_expense(description, amount)
    except ValueError as e:
        logger.error(f"Failed to process expense: {e}")
        return

    save_expense(
        description,
        normalized_amount,
        result["category"],
        result["confidence"]
    )
    if result["confidence"] == "low":
        logger.warning("Try again")

    logger.info("Expense successfully")
    print(f"saved: {description} -> {result['category']}, {result['confidence']}")

if __name__ == "__main__":
    main()