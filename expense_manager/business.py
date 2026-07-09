from expense_manager.manager import ExpenseManager

class BusinessExpenseManager(ExpenseManager):
    def __init__(self, tax_rate):
        super().__init__()
        self.tax_rate = tax_rate
    
    def get_total_with_tax(self):
        return int(self.get_total() * (1 + self.tax_rate))
    
    def __str__(self):
        total = self.get_total()
        total_with_tax = self.get_total_with_tax()
        return f"{super().__str__()}, Tax: Rp{total_with_tax - total}, Total with tax: Rp{total_with_tax}"