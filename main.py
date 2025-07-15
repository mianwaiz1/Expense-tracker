from expense_manager import ExpenseManager
from category_manager import CategoryManager
from reports import generate_reports
from visualizer import visualize_data

def main():
    expense_manager = ExpenseManager()
    category_manager = CategoryManager()

    while True:
        print("\n📋 Personal Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. Import Expenses from CSV")
        print("5. Add Category")
        print("6. Update Budget")
        print("7. Generate Report")
        print("8. Visualize Category Spending (Pie Chart)")
        print("9. Visualize Monthly Trends & Budget (Bar Charts)")
        print("10. Exit")


        choice = input("Enter your choice: ")
        try:
            if choice == '1':
                amount = float(input("Amount: "))
                category = input("Category: ")
                description = input("Description: ")
                date = input("Date (YYYY-MM-DD): ")
                expense_manager.add_expense(amount, category, description, date)

            elif choice == '2':
                print(expense_manager.df)
                index = int(input("Enter index to edit: "))
                field = input("Field to edit (Amount/Category/Description/Date): ")
                value = input(f"New value for {field}: ")
                expense_manager.edit_expense(index, **{field: value})

            elif choice == '3':
                print(expense_manager.df)
                index = int(input("Enter index to delete: "))
                expense_manager.delete_expense(index)

            elif choice == '4':
                path = input("Enter CSV filepath: ")
                expense_manager.import_expenses(path)

            elif choice == '5':
                name = input("Category name: ")
                budget = float(input("Budget amount: "))
                category_manager.add_category(name, budget)

            elif choice == '6':
                name = input("Category name to update: ")
                budget = float(input("New budget amount: "))
                category_manager.update_budget(name, budget)

            elif choice == '7':
                generate_reports(expense_manager.df, category_manager.df)

            elif choice == '8':
                visualize_data(expense_manager.df, category_manager.df, mode='category')

            elif choice == '9':
                visualize_data(expense_manager.df, category_manager.df, mode='monthly')

            elif choice == '10':
                print("👋 Exiting...")
                break

            else:
                print("❌ Invalid choice. Try again.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
