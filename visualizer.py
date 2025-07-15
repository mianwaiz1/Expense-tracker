import matplotlib.pyplot as plt
import pandas as pd

def visualize_data(expenses, categories, mode='all'):
    try:
        if expenses.empty:
            print("⚠️ No expenses to visualize.")
            return

        expenses['Date'] = pd.to_datetime(expenses['Date'], errors='coerce')
        expenses = expenses.dropna(subset=['Date'])

        if mode in ['category', 'all']:
            try:
                category_data = expenses.groupby('Category')['Amount'].sum()
                category_data.plot.pie(autopct='%1.1f%%', figsize=(6, 6))
                plt.title("Spending by Category")
                plt.ylabel('')
                plt.tight_layout()
                plt.show()
                print(f"Most spending: {category_data.idxmax()}")
            except Exception as e:
                print(f"❌ Pie chart error: {e}")

        if mode in ['monthly', 'all']:
            try:
                monthly_data = expenses.groupby([pd.Grouper(key='Date', freq='ME'), 'Category'])['Amount'].sum().unstack(fill_value=0)
                monthly_data.plot(kind='bar', stacked=True, figsize=(10, 6))
                plt.title("Monthly Spending by Category")
                plt.tight_layout()
                plt.show()
            except Exception as e:
                print(f"❌ Monthly chart error: {e}")

            try:
                if not categories.empty:
                    actual = expenses.groupby('Category')['Amount'].sum()
                    budget = categories.set_index('Category')['Budget']
                    all_categories = actual.index.union(budget.index)
                    actual = actual.reindex(all_categories, fill_value=0)
                    budget = budget.reindex(all_categories, fill_value=0)
                    df = pd.DataFrame({'Actual': actual, 'Budget': budget})
                    df.plot(kind='bar', figsize=(10, 6))
                    plt.title("Budget vs Actual Spending")
                    plt.tight_layout()
                    plt.show()
            except Exception as e:
                print(f"❌ Budget chart error: {e}")
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
