import pandas as pd
import os

class ExpenseManager:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.df = pd.DataFrame({
            'Amount': pd.Series(dtype='float'),
            'Category': pd.Series(dtype='str'),
            'Description': pd.Series(dtype='str'),
            'Date': pd.Series(dtype='datetime64[ns]')
        })
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filename):
                self.df = pd.read_csv(self.filename)
                self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
                self.df.dropna(subset=['Date'], inplace=True)
        except Exception as e:
            print(f"❌ Failed to load expenses: {e}")

    def save(self):
        try:
            self.df.to_csv(self.filename, index=False)
        except Exception as e:
            print(f"❌ Failed to save expenses: {e}")

    def add_expense(self, amount, category, description, date):
        try:
            date = pd.to_datetime(date, errors='coerce')
            if pd.isna(date):
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            new_row = pd.DataFrame([{
                'Amount': amount,
                'Category': category.strip().title(),
                'Description': description.strip(),
                'Date': date
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save()
            print("✅ Expense added successfully.")
        except Exception as e:
            print(f"❌ Failed to add expense: {e}")

    def edit_expense(self, index, **kwargs):
        try:
            if index not in self.df.index:
                print("❌ Invalid index.")
                return
            for key, value in kwargs.items():
                if key == 'Date':
                    value = pd.to_datetime(value, errors='coerce')
                    if pd.isna(value):
                        raise ValueError("Invalid date format.")
                if key == 'Amount':
                    value = float(value)
                self.df.at[index, key] = value
            self.save()
            print("✅ Expense updated.")
        except Exception as e:
            print(f"❌ Failed to edit expense: {e}")

    def delete_expense(self, index):
        try:
            self.df.drop(index, inplace=True)
            self.save()
            print("✅ Expense deleted.")
        except Exception as e:
            print(f"❌ Failed to delete expense: {e}")

    def import_expenses(self, filepath):
        try:
            new_data = pd.read_csv(filepath)
            new_data['Date'] = pd.to_datetime(new_data['Date'], errors='coerce')
            new_data.dropna(subset=['Date'], inplace=True)
            self.df = pd.concat([self.df, new_data], ignore_index=True)
            self.save()
            print("✅ Expenses imported from CSV.")
        except Exception as e:
            print(f"❌ Failed to import expenses: {e}")
