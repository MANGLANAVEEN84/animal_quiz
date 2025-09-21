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
        for i in range(3):
            btn = tk.Button(self.images_frame, command=lambda idx=i: self.on_choice(idx))
            btn.grid(row=0, column=i, padx=10)
            self.buttons.append(btn)

        self.feedback_var = tk.StringVar()
        self.feedback_label = tk.Label(self, textvariable=self.feedback_var, font=("Arial", 14))
        self.feedback_label.pack(pady=6)


