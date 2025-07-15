import pandas as pd
import os

class CategoryManager:
    def __init__(self, filename='catog.csv'):
        self.filename = filename
        self.df = pd.DataFrame(columns=['Category', 'Budget'])
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filename):
                self.df = pd.read_csv(self.filename)
                if 'Category' not in self.df.columns or 'Budget' not in self.df.columns:
                    self.df = pd.DataFrame(columns=['Category', 'Budget'])
            else:
                self.df = pd.DataFrame(columns=['Category', 'Budget'])
                self.save()
        except Exception as e:
            print(f"❌ Failed to load categories: {e}")

    def save(self):
        try:
            self.df.to_csv(self.filename, index=False)
        except Exception as e:
            print(f"❌ Failed to save categories: {e}")
