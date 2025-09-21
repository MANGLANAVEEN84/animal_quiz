import streamlit as st
import random

st.set_page_config(page_title="Number Comparison Quiz")
st.title("Which Number is Greater?")

# Generate 5 unique random pairs for the session
if 'quiz_pairs' not in st.session_state:
    pairs = set()
    while len(pairs) < 5:
        a, b = random.sample(range(1, 101), 2)
        pair = tuple(sorted((a, b)))
        pairs.add(pair)
    # For each pair, randomly decide if the greater number is on the left or right
    quiz_pairs = []
    for pair in list(pairs):
        a, b = pair
        if random.choice([True, False]):
            quiz_pairs.append((a, b))
        else:
            quiz_pairs.append((b, a))
    st.session_state.quiz_pairs = quiz_pairs
    st.session_state.answers = [""] * 5
    st.session_state.submitted = False

quiz_pairs = st.session_state.quiz_pairs
answers = st.session_state.answers
submitted = st.session_state.submitted

# Helper to draw a number in a circle
from PIL import Image, ImageDraw, ImageFont
import io

def draw_circle_number(num):
    img = Image.new('RGB', (120, 120), color='white')
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 112, 112), outline='black', width=6)
    try:
        font = ImageFont.truetype("arialbd.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
    bbox = font.getbbox(str(num)) if hasattr(font, 'getbbox') else draw.textbbox((0,0), str(num), font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((120-w)/2, (120-h)/2), str(num), fill='blue', font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

with st.form("quiz_form"):
    for i, (a, b) in enumerate(quiz_pairs):
        st.markdown(f"### Question {i+1}")
        cols = st.columns(2)
        # Radio group above the numbers
        selected = st.radio(
            label="Select the greater number:",
            options=[a, b],
            key=f"radio_{i}",
            horizontal=True,
            index=[a, b].index(answers[i]) if answers[i] in [a, b] else 0
        )
        answers[i] = selected
        with cols[0]:
            st.image(draw_circle_number(a), width=120)
        with cols[1]:
            st.image(draw_circle_number(b), width=120)
    submitted = st.form_submit_button("Submit")
    if submitted:
        if any(ans not in ["Left", "Right"] for ans in answers):
            st.error("Please select one answer (Left or Right) for each question.")
            st.stop()
        st.session_state.submitted = True
        st.session_state.answers = answers.copy()

if st.session_state.submitted:
    st.header("Results:")
    correct = 0
    for i, (a, b) in enumerate(quiz_pairs):
        user_ans = st.session_state.answers[i]
        right_ans = "Left is greater" if a > b else "Right is greater"
        if user_ans == right_ans:
            st.success(f"Q{i+1}: Correct! {a} vs {b}")
            correct += 1
        else:
            st.error(f"Q{i+1}: Incorrect. {a} vs {b}. Correct: {right_ans}")
    st.info(f"You got {correct}/5 correct.")
    if st.button("Retake Quiz"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()