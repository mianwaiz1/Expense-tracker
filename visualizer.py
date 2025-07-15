import matplotlib.pyplot as plt
import pandas as pd


def visualize_data(expenses, categories, mode='all'):
    try:
        if expenses.empty:
            print("⚠️ No expenses to visualize.")
            return

        if 'Date' not in expenses.columns:
            print("❌ 'Date' column missing in expenses.")
            return

        expenses['Date'] = pd.to_datetime(expenses['Date'], errors='coerce')

        invalid_rows = expenses['Date'].isna().sum()
        if invalid_rows > 0:
            print(f"⚠️ Skipping {invalid_rows} expense(s) with invalid dates.")
            expenses = expenses.dropna(subset=['Date'])

        if expenses.empty:
            print("⚠️ All dates were invalid. Nothing to visualize.")
            return

        print("\n📊 Generating Charts...")

        if mode in ['category', 'all']:
            try:
                category_data = expenses.groupby('Category')['Amount'].sum()
                category_data.plot.pie(autopct='%1.1f%%', figsize=(6, 6))
                plt.title("Spending by Category")
                plt.ylabel('')
                plt.tight_layout()
                plt.show()

                print("\n📝 Insight:")
                top_category = category_data.idxmax()
                print(f"Most spending occurred in: {top_category} → {category_data[top_category]:.2f}")

            except Exception as e:
                print(f"❌ Error generating pie chart: {e}")

        if mode in ['monthly', 'all']:
            try:
                # Sum by month and category for stacked bar chart
                monthly_by_category = expenses.groupby([pd.Grouper(key='Date', freq='ME'), 'Category'])['Amount'].sum().unstack(fill_value=0)
                monthly_by_category.plot(kind='bar', stacked=True, figsize=(10, 6))
                plt.title("Monthly Spending by Category (Stacked)")
                plt.xlabel("Month")
                plt.ylabel("Amount Spent")
                plt.tight_layout()
                plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.show()

                print("\n📝 Insight:")
                monthly_totals = monthly_by_category.sum(axis=1)
                peak_month = monthly_totals.idxmax().strftime('%B %Y')
                print(f"Highest total spending occurred in: {peak_month} → {monthly_totals.max():.2f}")

            except Exception as e:
                print(f"❌ Error generating stacked monthly bar chart: {e}")

            try:
                if not categories.empty:
                    actual = expenses.groupby('Category')['Amount'].sum()
                    budget = categories.set_index('Category')['Budget']

                    # Align indexes to include all categories from both actual and budget
                    all_categories = actual.index.union(budget.index)
                    actual = actual.reindex(all_categories, fill_value=0)
                    budget = budget.reindex(all_categories, fill_value=0)

                    df_compare = pd.DataFrame({
                        'Actual': actual,
                        'Budget': budget
                    })

                    df_compare.plot(kind='bar', figsize=(10, 6))
                    plt.title("Budget vs Actual Spending per Category")
                    plt.ylabel("Amount")
                    plt.xlabel("Category")
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.show()

                    print("\n📝 Insight:")
                    over_budget = df_compare[df_compare['Actual'] > df_compare['Budget']]
                    if not over_budget.empty:
                        print("⚠️ You overspent in the following categories:")
                        for cat in over_budget.index:
                            print(f"- {cat}: Over by {df_compare.at[cat, 'Actual'] - df_compare.at[cat, 'Budget']:.2f}")
                    else:
                        print("✅ All spending is within budget.")

                else:
                    print("⚠️ No categories defined. Skipping budget chart.")
            except Exception as e:
                print(f"❌ Error generating budget comparison chart: {e}")

    except Exception as e:
        print(f"\n❌ Visualization failed due to unexpected error: {e}")
