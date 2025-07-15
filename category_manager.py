import pandas as pd
import os

class CategoryManager:
    def __init__(self, filename='categories.csv'):
        self.filename = filename
        self.df = pd.DataFrame({
            'Category': pd.Series(dtype='str'),
            'Budget': pd.Series(dtype='float')
        })
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filename):
                self.df = pd.read_csv(self.filename)
        except Exception as e:
            print(f"❌ Failed to load categories: {e}")

    def save(self):
        try:
            self.df.to_csv(self.filename, index=False)
        except Exception as e:
            print(f"❌ Failed to save categories: {e}")

    def add_category(self, name, budget):
        try:
            new_row = pd.DataFrame([{
                'Category': name.strip().title(),
                'Budget': float(budget)
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save()
            print("✅ Category added.")
        except Exception as e:
            print(f"❌ Failed to add category: {e}")

    def update_budget(self, category, budget):
        try:
            if category not in self.df['Category'].values:
                print("⚠️ Category not found.")
                return
            self.df.loc[self.df['Category'] == category, 'Budget'] = float(budget)
            self.save()
            print("✅ Budget updated.")
        except Exception as e:
            print(f"❌ Failed to update budget: {e}")
