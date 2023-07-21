import random
import tkinter as tk
from tkinter import messagebox

def generate_password():
    try:
        name = name_entry.get()
        total_length = int(length_entry.get())

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        password_list = []

        num_letters = random.randint(1, total_length - 2)
        num_symbols = random.randint(1, total_length - num_letters - 1)
        num_numbers = total_length - num_letters - num_symbols

        for char in range(num_letters):
            password_list.append(random.choice(letters))

        for char in range(num_symbols):
            password_list += random.choice(symbols)

        for char in range(num_numbers):
            password_list += random.choice(numbers)

        random.shuffle(password_list)
        password = "".join(password_list)
        password_display.config(text=f"your generated password is: {password}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI window
window = tk.Tk()
window.title("Password Generator")
# Labels and Input fields
name_label = tk.Label(window, text="Please enter user name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

length_label = tk.Label(window, text="Please enter password length:")
length_label.pack()
length_entry = tk.Entry(window)
length_entry.pack()

# Generate Password Button
generate_button = tk.Button(window, text="Generate Password", command=generate_password)
generate_button.pack()

# Password display
password_display = tk.Label(window, text=" ", font=("Arial", 14))
password_display.pack()

window.mainloop()
