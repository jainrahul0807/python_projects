import tkinter as tk
from tkinter import messagebox
from tkinter import END

def add_task():
    task = task_entry.get()
    if task.strip():
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    try:
        index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(index)
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def mark_completed():
    try:
        index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(index)
        tasks_listbox.delete(index)
        tasks_listbox.insert(tk.END, f"{task} (Completed)")
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

# Create the main application window
app = tk.Tk()
app.title("To-Do List")

# Create the components
tasks_listbox = tk.Listbox(app, selectmode=tk.SINGLE)
task_entry = tk.Entry(app)
add_button = tk.Button(app, text="Add Task", command=add_task)
delete_button = tk.Button(app, text="Delete Task", command=delete_task)
mark_button = tk.Button(app, text="Mark Completed", command=mark_completed)

# Place the components in the window
tasks_listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
task_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)
add_button.pack(padx=10, pady=5)
mark_button.pack(padx=5, pady=5)
delete_button.pack(padx=10, pady=5)


# Start the Tkinter event loop
app.mainloop()
