class ExpenseManager:

    def __init__(self):
        self.__expenses = []

    def add_expense(self, amount, category, description):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        elif category.strip() == "":
            raise ValueError("Category cannot be empty")
        elif description.strip() == "":
            raise ValueError("Description cannot be empty")
        
        expense = {
            "amount": amount,
            "category": category,
            "description": description
        }
        self.__expenses.append(expense)

    def get_expenses(self):
        return self.__expenses.copy()

    def get_total(self):
        return sum(expense["amount"] for expense in self.__expenses)

    def get_by_category(self, category):
        return [
            expense 
            for expense in self.__expenses 
            if expense["category"] == category
        ]
    
    def __str__(self):
        return f"{len(self.__expenses)} expenses, Total: Rp{self.get_total()}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(expenses={self.__expenses})"
    
    def __len__(self):
        return len(self.__expenses)
    
    def __eq__(self, other):
        if not isinstance(other, ExpenseManager):
            return False
        return self.__expenses == other.get_expenses()