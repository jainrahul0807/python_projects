import math
import tkinter as tk
from tkinter import messagebox

# Calculator operations
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero!"
    else:
        return a / b

def modulo(a, b):
    return a % b

calculator = {'+': add, '-': sub, '*': mult, '/': divide, '%': modulo}

def on_button_click(value):
    current_text = input_entry.get()
    if value == 'C':
        input_entry.delete(0, tk.END)
    elif value == '=':
        try:
            result = calculate_expression(current_text)
            input_entry.delete(0, tk.END)
            input_entry.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    elif value == 'x': 
        input_entry.delete(len(current_text) - 1, tk.END)
    else:
        input_entry.insert(tk.END, value)

def calculate_expression(expression):
    for key in calculator:
        expression = expression.replace(key, f" {key} ")
    return eval(expression)

# Create GUI window
window = tk.Tk()
window.title("Calculator")

# Calculator input entry
input_entry = tk.Entry(window, font=("Arial", 18))
input_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Calculator buttons
buttons = [
    '%', '/', '*', '-',
    '7', '8', '9','+',
    '4', '5', '6', '=',
    '1', '2', '3', 'x',
    'C', '0', '.'
]

row_index = 1
col_index = 0
for button_text in buttons:
    tk.Button(window, text=button_text, padx=20, pady=10, font=("Arial", 14),command=lambda value=button_text: on_button_click(value)).grid(row=row_index, column=col_index)
    col_index += 1
    if col_index > 3:
        col_index = 0
        row_index += 1

window.mainloop()
