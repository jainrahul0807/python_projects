import tkinter as tk
from tkinter import messagebox
questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["London", "Paris", "Berlin", "Madrid"],
        "correct_answer": 1
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Mercury"],
        "correct_answer": 1
    },
    {
        "question": "What is 2 + 2?",
        "choices": ["3", "4", "5", "6"],
        "correct_answer": 1
    }
]
current_question_index = 0
score = 0
def display_question():
    question_data = questions[current_question_index]
    question_label.config(text=f"Question {current_question_index+1}/{len(questions)}: {question_data['question']}")
    for i, choice in enumerate(question_data["choices"]):
        choices_radio_buttons[i].config(text=choice)
def check_answer():
    global score, current_question_index
    user_answer = int(tkvar.get())
    correct_answer = questions[current_question_index]["correct_answer"]
    if user_answer == correct_answer:
        score += 1
    current_question_index += 1
    if current_question_index >= len(questions):
        display_final_results()
    else:
        display_question()
def display_final_results():
    result = f"You got {score} out of {len(questions)} questions correct!"
    messagebox.showinfo("Quiz Complete", result)
app = tk.Tk()
app.title("Quiz Game")
welcome_label = tk.Label(app, text="Welcome to the Quiz Game!")
question_label = tk.Label(app, text="", wraplength=300)
choices_radio_buttons = []
tkvar = tk.StringVar(value="-1")  # Set default value to -1
for i in range(4):
    radio_button = tk.Radiobutton(app, variable=tkvar, value=str(i))
    choices_radio_buttons.append(radio_button)
next_button = tk.Button(app, text="Next", command=check_answer)
welcome_label.pack(pady=10)
question_label.pack(pady=3)
for radio_button in choices_radio_buttons:
    radio_button.pack(anchor=tk.W, side=tk.LEFT)
next_button.pack(padx=10, pady=10)
display_question()
app.mainloop()