import pandas as pd

def generate_reports(expenses, categories):
    try:
        if expenses.empty:
            print("⚠️ No expense data available.")
            return

        print("\n🗓️ Monthly Summary:")
        monthly = expenses.groupby(pd.Grouper(key='Date', freq='M'))['Amount'].sum()
        print(monthly)

        print("\n📁 Category Breakdown:")
        category_sum = expenses.groupby('Category')['Amount'].sum()
        print(category_sum)

        print("\n📈 Budget vs Actual:")
        for _, row in categories.iterrows():
            spent = expenses[expenses['Category'] == row['Category']]['Amount'].sum()
            budget = row['Budget']
            print(f"{row['Category']}: Budget = {budget}, Spent = {spent}, {'Over' if spent > budget else 'Under'} Budget")
    except Exception as e:
        print(f"❌ Failed to generate report: {e}")
