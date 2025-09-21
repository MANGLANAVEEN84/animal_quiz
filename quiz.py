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


