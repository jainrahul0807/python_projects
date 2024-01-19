import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Create and set up the UI components
        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_entry = ttk.Entry(root)
        self.category_label = ttk.Label(root, text="Category:")
        self.category_entry = ttk.Entry(root)
        self.description_label = ttk.Label(root, text="Description:")
        self.description_entry = ttk.Entry(root)
        self.record_button = ttk.Button(root, text="Record Expense", command=self.record_expense)

        self.expenses_treeview = ttk.Treeview(root, columns=('Date', 'Amount', 'Category', 'Description'), show='headings')
        self.expenses_treeview.heading('Date', text='Date', command=lambda: self.sort_expenses('date'))
        self.expenses_treeview.heading('Amount', text='Amount', command=lambda: self.sort_expenses('amount'))
        self.expenses_treeview.heading('Category', text='Category', command=lambda: self.sort_expenses('category'))
        self.expenses_treeview.heading('Description', text='Description', command=lambda: self.sort_expenses('description'))

        self.view_expenses_button = ttk.Button(root, text="View Expenses", command=self.view_expenses)
        self.view_category_button = ttk.Button(root, text="View by Category", command=self.view_by_category)
        self.view_pattern_button = ttk.Button(root, text="View Spending Pattern", command=self.view_spending_pattern)

        # Connect to SQLite database
        self.conn = sqlite3.connect('expenses.db')
        self.create_expenses_table()

        # Pack UI components
        self.amount_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.category_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.description_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.record_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.expenses_treeview.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        self.view_expenses_button.grid(row=5, column=0, pady=5)
        self.view_category_button.grid(row=5, column=1, pady=5)
        self.view_pattern_button.grid(row=6, column=0, columnspan=2, pady=5)

    def create_expenses_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def record_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        if amount and category:
            try:
                float(amount)
            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a valid number.")
                return

            date = datetime.datetime.now().strftime('%Y-%m-%d')
            expense = {'date': date, 'amount': amount, 'category': category, 'description': description}
            self.save_expense_to_database(expense)
            messagebox.showinfo("Expense Recorded", "Expense recorded successfully.")
            self.clear_entries()
            self.view_expenses()
        else:
            messagebox.showerror("Missing Information", "Amount and Category are required.")

    def save_expense_to_database(self, expense):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, description)
            VALUES (?, ?, ?, ?)
        ''', (expense['date'], expense['amount'], expense['category'], expense['description']))
        self.conn.commit()

    def view_expenses(self):
        for item in self.expenses_treeview.get_children():
            self.expenses_treeview.delete(item)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()

        for expense in expenses:
            self.expenses_treeview.insert('', 'end', values=(expense[1], expense[2], expense[3], expense[4]))

    def view_by_category(self):
        category_sums = {}
        cursor = self.conn.cursor()
        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        category_totals = cursor.fetchall()

        for category, total_amount in category_totals:
            category_sums[category] = total_amount

        self.show_category_totals(category_sums)

    def show_category_totals(self, category_sums):
        category_totals_window = tk.Toplevel(self.root)
        category_totals_window.title("Category Totals")

        treeview = ttk.Treeview(category_totals_window, columns=('Category', 'Total Amount'), show='headings')
        treeview.heading('Category', text='Category')
        treeview.heading('Total Amount', text='Total Amount')

        for category, total_amount in category_sums.items():
            treeview.insert('', 'end', values=(category, total_amount))

        treeview.pack(padx=10, pady=10)

    def view_spending_pattern(self):
        pattern_window = tk.Toplevel(self.root)
        pattern_window.title("Spending Pattern Over Time")

        cursor = self.conn.cursor()
        cursor.execute('SELECT strftime("%Y-%m", date) AS month, SUM(amount) FROM expenses GROUP BY month')
        pattern_data = cursor.fetchall()

        months = []
        amounts = []

        for month, total_amount in pattern_data:
            months.append(month)
            amounts.append(total_amount)

        fig, ax = plt.subplots()
        ax.plot(months, amounts, marker='o')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Amount')
        ax.set_title('Spending Pattern Over Time')

        canvas = FigureCanvasTkAgg(fig, master=pattern_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(padx=10, pady=10)

        canvas.draw()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def sort_expenses(self, column):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM expenses ORDER BY {column}')
        expenses = cursor.fetchall()
        self.view_expenses()
        for expense in expenses:
            self.expenses_treeview.insert('', 'end', values=(expense[1], expense[2], expense[3], expense[4]))

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

