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

