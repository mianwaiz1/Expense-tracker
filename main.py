import json
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Optional, Tuple

class ExpenseTracker:
    def __init__(self, data_file='expenses.json', categories_file='categories.json'):
        self.data_file = data_file
        self.categories_file = categories_file
        self.expenses = self.load_expenses()
        self.categories = self.load_categories()
        
        # Initialize default categories if none exist
        if not self.categories:
            self.initialize_default_categories()
    
    def load_expenses(self) -> List[Dict]:
        """Load expenses from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_expenses(self):
        """Save expenses to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def load_categories(self) -> Dict:
        """Load categories and budgets from JSON file"""
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_categories(self):
        """Save categories to JSON file"""
        with open(self.categories_file, 'w') as f:
            json.dump(self.categories, f, indent=2)
    
    def initialize_default_categories(self):
        """Initialize with default categories"""
        default_categories = {
            'Food': {'budget': 500.0, 'description': 'Groceries, dining out, snacks'},
            'Transport': {'budget': 200.0, 'description': 'Gas, public transport, parking'},
            'Entertainment': {'budget': 150.0, 'description': 'Movies, games, hobbies'},
            'Healthcare': {'budget': 100.0, 'description': 'Medical expenses, pharmacy'},
            'Shopping': {'budget': 300.0, 'description': 'Clothing, electronics, misc'},
            'Bills': {'budget': 800.0, 'description': 'Rent, utilities, subscriptions'},
            'Other': {'budget': 100.0, 'description': 'Miscellaneous expenses'}
        }
        self.categories = default_categories
        self.save_categories()
    
    def add_expense(self, amount: float, category: str, description: str, date: str = None):
        """Add a new expense"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Validate category
        if category not in self.categories:
            print(f"Warning: Category '{category}' doesn't exist. Creating new category.")
            self.categories[category] = {'budget': 0.0, 'description': ''}
            self.save_categories()
        
        expense = {
            'id': len(self.expenses) + 1,
            'amount': amount,
            'category': category,
            'description': description,
            'date': date,
            'created_at': datetime.now().isoformat()
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        print(f"✓ Expense added: ${amount:.2f} for {category}")
    
    def edit_expense(self, expense_id: int, **kwargs):
        """Edit an existing expense"""
        for expense in self.expenses:
            if expense['id'] == expense_id:
                for key, value in kwargs.items():
                    if key in expense:
                        expense[key] = value
                expense['updated_at'] = datetime.now().isoformat()
                self.save_expenses()
                print(f"✓ Expense {expense_id} updated")
                return
        print(f"❌ Expense {expense_id} not found")
    
    def delete_expense(self, expense_id: int):
        """Delete an expense"""
        for i, expense in enumerate(self.expenses):
            if expense['id'] == expense_id:
                deleted = self.expenses.pop(i)
                self.save_expenses()
                print(f"✓ Deleted expense: ${deleted['amount']:.2f} for {deleted['category']}")
                return
        print(f"❌ Expense {expense_id} not found")
    
    def import_from_csv(self, file_path: str):
        """Import expenses from CSV file"""
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    try:
                        amount = float(row['amount'])
                        category = row['category']
                        description = row['description']
                        date = row.get('date', datetime.now().strftime('%Y-%m-%d'))
                        
                        self.add_expense(amount, category, description, date)
                        count += 1
                    except (ValueError, KeyError) as e:
                        print(f"Error processing row {row}: {e}")
                        continue
                
                print(f"✓ Imported {count} expenses from {file_path}")
                
        except FileNotFoundError:
            print(f"❌ File {file_path} not found")
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
    
    def create_category(self, name: str, budget: float = 0.0, description: str = ''):
        """Create a new category"""
        if name in self.categories:
            print(f"❌ Category '{name}' already exists")
            return
        
        self.categories[name] = {
            'budget': budget,
            'description': description
        }
        self.save_categories()
        print(f"✓ Category '{name}' created with budget ${budget:.2f}")
    
    def set_budget(self, category: str, budget: float):
        """Set budget for a category"""
        if category not in self.categories:
            print(f"❌ Category '{category}' doesn't exist")
            return
        
        self.categories[category]['budget'] = budget
        self.save_categories()
        print(f"✓ Budget for '{category}' set to ${budget:.2f}")
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get monthly spending summary"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        monthly_expenses = [
            exp for exp in self.expenses
            if start_date <= datetime.strptime(exp['date'], '%Y-%m-%d') < end_date
        ]
        
        summary = {
            'total_spent': sum(exp['amount'] for exp in monthly_expenses),
            'total_expenses': len(monthly_expenses),
            'category_breakdown': defaultdict(float),
            'daily_breakdown': defaultdict(float)
        }
        
        for expense in monthly_expenses:
            summary['category_breakdown'][expense['category']] += expense['amount']
            summary['daily_breakdown'][expense['date']] += expense['amount']
        
        return summary
    
    def get_category_analysis(self, category: str, days: int = 30) -> Dict:
        """Analyze spending for a specific category"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        category_expenses = [
            exp for exp in self.expenses
            if exp['category'] == category and 
            datetime.strptime(exp['date'], '%Y-%m-%d') >= cutoff_date
        ]
        
        if not category_expenses:
            return {'error': f'No expenses found for category "{category}" in the last {days} days'}
        
        total_spent = sum(exp['amount'] for exp in category_expenses)
        avg_per_expense = total_spent / len(category_expenses)
        
        return {
            'category': category,
            'total_spent': total_spent,
            'expense_count': len(category_expenses),
            'average_per_expense': avg_per_expense,
            'budget': self.categories.get(category, {}).get('budget', 0),
            'budget_used_percent': (total_spent / self.categories.get(category, {}).get('budget', 1)) * 100,
            'expenses': category_expenses
        }
    
    def get_budget_status(self, year: int, month: int) -> Dict:
        """Get budget vs actual spending comparison"""
        monthly_summary = self.get_monthly_summary(year, month)
        budget_status = {}
        
        for category, budget_info in self.categories.items():
            spent = monthly_summary['category_breakdown'].get(category, 0)
            budget = budget_info['budget']
            
            budget_status[category] = {
                'budget': budget,
                'spent': spent,
                'remaining': budget - spent,
                'percent_used': (spent / budget * 100) if budget > 0 else 0,
                'over_budget': spent > budget
            }
        
        return budget_status
    
    def find_spending_trends(self, days: int = 90) -> Dict:
        """Identify spending trends and patterns"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_expenses = [
            exp for exp in self.expenses
            if datetime.strptime(exp['date'], '%Y-%m-%d') >= cutoff_date
        ]
        
        if not recent_expenses:
            return {'error': 'No recent expenses found'}
        
        # Weekly spending pattern
        weekly_spending = defaultdict(float)
        category_trends = defaultdict(list)
        
        for expense in recent_expenses:
            date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
            week_start = date_obj - timedelta(days=date_obj.weekday())
            week_key = week_start.strftime('%Y-%m-%d')
            
            weekly_spending[week_key] += expense['amount']
            category_trends[expense['category']].append(expense['amount'])
        
        # Calculate trends
        avg_weekly_spending = sum(weekly_spending.values()) / len(weekly_spending)
        
        category_averages = {
            cat: sum(amounts) / len(amounts) 
            for cat, amounts in category_trends.items()
        }
        
        return {
            'avg_weekly_spending': avg_weekly_spending,
            'category_averages': category_averages,
            'weekly_spending': dict(weekly_spending),
            'total_expenses': len(recent_expenses),
            'total_spent': sum(exp['amount'] for exp in recent_expenses)
        }
    
    def visualize_category_breakdown(self, year: int, month: int):
        """Create pie chart for category breakdown"""
        summary = self.get_monthly_summary(year, month)
        
        if not summary['category_breakdown']:
            print("No expenses found for the specified month")
            return
        
        categories = list(summary['category_breakdown'].keys())
        amounts = list(summary['category_breakdown'].values())
        
        plt.figure(figsize=(10, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title(f'Expense Breakdown - {year}-{month:02d}')
        plt.axis('equal')
        plt.show()
    
    def visualize_spending_trends(self, days: int = 30):
        """Create bar chart for daily spending trends"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        daily_spending = defaultdict(float)
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if expense_date >= cutoff_date:
                daily_spending[expense['date']] += expense['amount']
        
        if not daily_spending:
            print("No expenses found for the specified period")
            return
        
        dates = sorted(daily_spending.keys())
        amounts = [daily_spending[date] for date in dates]
        
        plt.figure(figsize=(12, 6))
        plt.bar(dates, amounts)
        plt.title(f'Daily Spending Trends (Last {days} days)')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def visualize_budget_comparison(self, year: int, month: int):
        """Create bar chart comparing budget vs actual spending"""
        budget_status = self.get_budget_status(year, month)
        
        categories = list(budget_status.keys())
        budgets = [budget_status[cat]['budget'] for cat in categories]
        spent = [budget_status[cat]['spent'] for cat in categories]
        
        x = range(len(categories))
        width = 0.35
        
        plt.figure(figsize=(12, 8))
        plt.bar([i - width/2 for i in x], budgets, width, label='Budget', alpha=0.7)
        plt.bar([i + width/2 for i in x], spent, width, label='Spent', alpha=0.7)
        
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.title(f'Budget vs Actual Spending - {year}-{month:02d}')
        plt.xticks(x, categories, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def display_expenses(self, limit: int = 10):
        """Display recent expenses"""
        if not self.expenses:
            print("No expenses found")
            return
        
        sorted_expenses = sorted(self.expenses, key=lambda x: x['date'], reverse=True)
        
        print(f"\n{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("-" * 80)
        
        for expense in sorted_expenses[:limit]:
            print(f"{expense['id']:<5} {expense['date']:<12} {expense['category']:<15} "
                  f"${expense['amount']:<9.2f} {expense['description']:<30}")
    
    def display_categories(self):
        """Display all categories with budgets"""
        if not self.categories:
            print("No categories found")
            return
        
        print(f"\n{'Category':<20} {'Budget':<10} {'Description':<30}")
        print("-" * 70)
        
        for category, info in self.categories.items():
            print(f"{category:<20} ${info['budget']:<9.2f} {info['description']:<30}")


def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n" + "="*50)
        print("       PERSONAL EXPENSE TRACKER")
        print("="*50)
        print("1.  Add Expense")
        print("2.  Edit Expense")
        print("3.  Delete Expense")
        print("4.  View Recent Expenses")
        print("5.  Import from CSV")
        print("6.  Create Category")
        print("7.  Set Budget")
        print("8.  View Categories")
        print("9.  Monthly Summary")
        print("10. Category Analysis")
        print("11. Budget Status")
        print("12. Spending Trends")
        print("13. Visualize Category Breakdown")
        print("14. Visualize Spending Trends")
        print("15. Visualize Budget Comparison")
        print("16. Exit")
        
        choice = input("\nEnter your choice (1-16): ").strip()
        
        try:
            if choice == '1':
                amount = float(input("Enter amount: $"))
                category = input("Enter category: ").strip()
                description = input("Enter description: ").strip()
                date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                
                if not date:
                    date = None
                
                tracker.add_expense(amount, category, description, date)
            
            elif choice == '2':
                expense_id = int(input("Enter expense ID to edit: "))
                print("Leave blank to keep current value")
                
                amount = input("New amount: $").strip()
                category = input("New category: ").strip()
                description = input("New description: ").strip()
                date = input("New date (YYYY-MM-DD): ").strip()
                
                kwargs = {}
                if amount:
                    kwargs['amount'] = float(amount)
                if category:
                    kwargs['category'] = category
                if description:
                    kwargs['description'] = description
                if date:
                    kwargs['date'] = date
                
                tracker.edit_expense(expense_id, **kwargs)
            
            elif choice == '3':
                expense_id = int(input("Enter expense ID to delete: "))
                confirm = input("Are you sure? (y/N): ").strip().lower()
                if confirm == 'y':
                    tracker.delete_expense(expense_id)
            
            elif choice == '4':
                limit = input("Number of expenses to show (default 10): ").strip()
                limit = int(limit) if limit else 10
                tracker.display_expenses(limit)
            
            elif choice == '5':
                file_path = input("Enter CSV file path: ").strip()
                tracker.import_from_csv(file_path)
            
            elif choice == '6':
                name = input("Enter category name: ").strip()
                budget = input("Enter budget amount: $").strip()
                budget = float(budget) if budget else 0.0
                description = input("Enter description: ").strip()
                tracker.create_category(name, budget, description)
            
            elif choice == '7':
                category = input("Enter category name: ").strip()
                budget = float(input("Enter budget amount: $"))
                tracker.set_budget(category, budget)
            
            elif choice == '8':
                tracker.display_categories()
            
            elif choice == '9':
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                summary = tracker.get_monthly_summary(year, month)
                
                print(f"\nMonthly Summary for {year}-{month:02d}")
                print("-" * 40)
                print(f"Total Spent: ${summary['total_spent']:.2f}")
                print(f"Total Expenses: {summary['total_expenses']}")
                print("\nCategory Breakdown:")
                for category, amount in summary['category_breakdown'].items():
                    print(f"  {category}: ${amount:.2f}")
            
            elif choice == '10':
                category = input("Enter category name: ").strip()
                days = input("Number of days to analyze (default 30): ").strip()
                days = int(days) if days else 30
                
                analysis = tracker.get_category_analysis(category, days)
                
                if 'error' in analysis:
                    print(f"❌ {analysis['error']}")
                else:
                    print(f"\nCategory Analysis: {analysis['category']}")
                    print("-" * 40)
                    print(f"Total Spent: ${analysis['total_spent']:.2f}")
                    print(f"Number of Expenses: {analysis['expense_count']}")
                    print(f"Average per Expense: ${analysis['average_per_expense']:.2f}")
                    print(f"Budget: ${analysis['budget']:.2f}")
                    print(f"Budget Used: {analysis['budget_used_percent']:.1f}%")
            
            elif choice == '11':
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                
                budget_status = tracker.get_budget_status(year, month)
                
                print(f"\nBudget Status for {year}-{month:02d}")
                print("-" * 70)
                print(f"{'Category':<15} {'Budget':<10} {'Spent':<10} {'Remaining':<12} {'% Used':<8}")
                print("-" * 70)
                
                for category, status in budget_status.items():
                    over_budget = "⚠️" if status['over_budget'] else ""
                    print(f"{category:<15} ${status['budget']:<9.2f} ${status['spent']:<9.2f} "
                          f"${status['remaining']:<11.2f} {status['percent_used']:<7.1f}% {over_budget}")
            
            elif choice == '12':
                days = input("Number of days to analyze (default 90): ").strip()
                days = int(days) if days else 90
                
                trends = tracker.find_spending_trends(days)
                
                if 'error' in trends:
                    print(f"❌ {trends['error']}")
                else:
                    print(f"\nSpending Trends (Last {days} days)")
                    print("-" * 40)
                    print(f"Average Weekly Spending: ${trends['avg_weekly_spending']:.2f}")
                    print(f"Total Expenses: {trends['total_expenses']}")
                    print(f"Total Spent: ${trends['total_spent']:.2f}")
                    print("\nCategory Averages:")
                    for category, avg in trends['category_averages'].items():
                        print(f"  {category}: ${avg:.2f}")
            
            elif choice == '13':
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                tracker.visualize_category_breakdown(year, month)
            
            elif choice == '14':
                days = input("Number of days (default 30): ").strip()
                days = int(days) if days else 30
                tracker.visualize_spending_trends(days)
            
            elif choice == '15':
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                tracker.visualize_budget_comparison(year, month)
            
            elif choice == '16':
                print("Thank you for using Personal Expense Tracker!")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
