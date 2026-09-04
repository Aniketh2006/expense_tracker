import json

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        f = open("expenses.json")
        self.expenses = json.load(f)

    def add_expense(self, amount, category, description):
        entry = {"amount": amount, "category": category, "description": description}
        self.expenses.append(entry)

    def get_total(self):
        total = 0
        for e in self.expenses:
            total = total + e["amount"]
        return total

    def get_average(self):
        return self.get_total() / len(self.expenses)

    def get_by_category(self, category):
        result = []
        for e in self.expenses:
            if e["category"] = category:
                result.append(e)
        return result

    def save(self):
        f = open("expenses.json", "w")
        json.dump(self.expenses, f)


tracker = ExpenseTracker()
tracker.add_expense(-500, "Food", "groceries")
print(tracker.get_average())
