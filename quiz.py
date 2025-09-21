def generate_quiz(num_questions: int = 5):
    """Generate a list of quiz questions for the Streamlit app.
    Each question is a tuple: (question_text, options, answer)
    """
    from animals import get_random_question
    quiz = []
    for _ in range(num_questions):
        answer, options = get_random_question()
        question = f"Which one is {answer}?"
        quiz.append((question, options, answer))
    return quiz

import random
import tkinter as tk
from tkinter import messagebox
from typing import List

from PIL import ImageTk

from animals import get_random_question
from image_fetcher import get_animal_image

APP_TITLE = "Animal Alphabet Quiz"
IMG_SIZE = (320, 240)


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1040x520")  # Enough space for 3 images side-by-side
        self.resizable(False, False)

        self.correct_answer: str | None = None
        self.options: List[str] = []
        self.photo_refs: List[ImageTk.PhotoImage] = []

        self.header = tk.Label(self, text=APP_TITLE, font=("Arial", 18, "bold"))
        self.header.pack(pady=8)

        self.question_var = tk.StringVar()
        self.question_label = tk.Label(self, textvariable=self.question_var, font=("Arial", 16))
        self.question_label.pack(pady=6)

        self.images_frame = tk.Frame(self)
        self.images_frame.pack(pady=10)

        self.buttons: List[tk.Button] = []
        for i in range(3):
            btn = tk.Button(self.images_frame, command=lambda idx=i: self.on_choice(idx))
            btn.grid(row=0, column=i, padx=10)
            self.buttons.append(btn)

        self.feedback_var = tk.StringVar()
        self.feedback_label = tk.Label(self, textvariable=self.feedback_var, font=("Arial", 14))
        self.feedback_label.pack(pady=6)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(pady=8)

        self.next_btn = tk.Button(self.controls_frame, text="Next Question", command=self.new_question)
        self.next_btn.grid(row=0, column=0, padx=5)

        self.quit_btn = tk.Button(self.controls_frame, text="Quit", command=self.destroy)
        self.quit_btn.grid(row=0, column=1, padx=5)

        self.new_question()

    def new_question(self):
        self.feedback_var.set("")
        self.enable_buttons(True)
        correct, opts = get_random_question()
        self.correct_answer = correct
        self.options = opts
        self.question_var.set(f"Identify the animal: {correct}")
        self.load_images()

    def load_images(self):
        # Clear old images
        self.photo_refs.clear()
        for i, name in enumerate(self.options):
            img = get_animal_image(name, IMG_SIZE)
            photo = ImageTk.PhotoImage(img)
            self.photo_refs.append(photo)
            self.buttons[i].configure(image=photo, text=name, compound=tk.TOP, width=IMG_SIZE[0], height=IMG_SIZE[1]+30)

    def enable_buttons(self, enable: bool):
        state = tk.NORMAL if enable else tk.DISABLED
        for b in self.buttons:
            b.configure(state=state)

    def on_choice(self, idx: int):
        chosen = self.options[idx]
        if chosen == self.correct_answer:
            self.feedback_var.set("Correct!")
        else:
            self.feedback_var.set(f"Incorrect. The correct answer is {self.correct_answer}.")
        self.enable_buttons(False)


if __name__ == "__main__":
    try:
        app = QuizApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
