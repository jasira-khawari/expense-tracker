import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "expenses.json"

# ---------- Data ----------
def load_expenses():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)
    return []

def save_expenses():
    with open(FILE, "w") as file:
        json.dump(expenses, file, indent=4)

expenses = load_expenses()


# ---------- Functions ----------
def add_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_var.get()

    if not name or not amount:
        messagebox.showwarning("Missing Information",
                               "Please enter the expense and amount.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    expenses.append({
        "name": name,
        "amount": amount,
        "category": category
    })

    save_expenses()

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    update_display()


def delete_expense():
    selected = expense_list.curselection()

    if not selected:
        messagebox.showwarning("Select Expense",
                               "Please select an expense to delete.")
        return

    expenses.pop(selected[0])
    save_expenses()
    update_display()


def update_display():
    expense_list.delete(0, tk.END)

    total = 0

    for expense in expenses:
        text = (
            f"{expense['name']} | "
            f"Rs. {expense['amount']:.2f} | "
            f"{expense['category']}"
        )

        expense_list.insert(tk.END, text)
        total += expense["amount"]

    total_label.config(text=f"Total Spent: Rs. {total:.2f}")


# ---------- App ----------
app = tk.Tk()
app.title("My Expense Tracker")
app.geometry("550x600")
app.resizable(False, False)

title = tk.Label(
    app,
    text="Expense Tracker",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)


# Expense name
tk.Label(app, text="Expense Name").pack()

name_entry = tk.Entry(app, width=40)
name_entry.pack(pady=5)


# Amount
tk.Label(app, text="Amount (Rs.)").pack()

amount_entry = tk.Entry(app, width=40)
amount_entry.pack(pady=5)


# Category
tk.Label(app, text="Category").pack()

category_var = tk.StringVar(value="Food")

categories = ["Food", "Transport", "Shopping", "Education", "Other"]

category_menu = tk.OptionMenu(
    app,
    category_var,
    *categories
)

category_menu.pack(pady=5)


# Buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=15)

add_button = tk.Button(
    button_frame,
    text="Add Expense",
    command=add_expense,
    width=15
)

add_button.grid(row=0, column=0, padx=5)


delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    command=delete_expense,
    width=15
)

delete_button.grid(row=0, column=1, padx=5)


# Expense list
tk.Label(
    app,
    text="Your Expenses",
    font=("Arial", 14, "bold")
).pack(pady=10)

expense_list = tk.Listbox(
    app,
    width=65,
    height=15
)

expense_list.pack()


# Total
total_label = tk.Label(
    app,
    text="Total Spent: Rs. 0.00",
    font=("Arial", 16, "bold")
)

total_label.pack(pady=20)


# Load saved data
update_display()

app.mainloop()