
import streamlit as st

from animals import get_animal_list
from quiz import generate_quiz
import os
from PIL import Image

def get_preloaded_image(animal_name, size=(320, 240)):
    fname = animal_name.strip().lower().replace(" ", "_") + ".png"
    fpath = os.path.join(os.path.dirname(__file__), "preloaded_images", fname)
    if os.path.exists(fpath):
        img = Image.open(fpath).convert("RGB")
        img = img.resize(size)
        return img
    else:
        # fallback: blank image
        return Image.new("RGB", size, (200, 200, 200))
from PIL import Image
from email_utils import generate_code, send_verification_email
import re
import time



st.title("ABC Quiz")


# Require user name and email before starting quiz
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'user_email' not in st.session_state:
    st.session_state.user_email = ''
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'email_verified' not in st.session_state:
    st.session_state.email_verified = False
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = ''
if 'code_sent_time' not in st.session_state:
    st.session_state.code_sent_time = 0

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# Optional user image upload
if 'user_image' not in st.session_state:
    st.session_state.user_image = None

if not st.session_state.quiz_started:
    # User credential and email verification temporarily disabled
    st.session_state.quiz_started = True

def get_letter_image(letter, size=(200, 200)):
    fname = f"{letter.upper()}.png"
    fpath = os.path.join(os.path.dirname(__file__), "letterimage", fname)
    if os.path.exists(fpath):
        img = Image.open(fpath).convert("RGB")
        img = img.resize(size)
        return img
    else:
        return Image.new("RGB", size, (220, 220, 220))

# Fruit names for A-Z
FRUITS = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew", "Indian Fig", "Jackfruit", "Kiwi", "Lemon", "Mango", "Nectarine", "Orange", "Papaya", "Quince", "Raspberry", "Strawberry", "Tomato", "Ugli Fruit", "Vanilla", "Watermelon", "Xigua", "Yellow Passion Fruit", "Zucchini"
]
def get_fruit_name(letter):
    idx = ord(letter.upper()) - ord('A')
    if 0 <= idx < len(FRUITS):
        return FRUITS[idx]
    return ""

tab1, tab2, tab3, tab4 = st.tabs(["Quiz", "Animals", "ABC Sequence Quiz", "Number Quiz"])


with tab3:
    st.header("ABC Sequence / Missing Letter Quiz")
    import random
    letters = [chr(ord('A') + i) for i in range(26)]
    max_questions = 5
    if 'abc_quiz_questions' not in st.session_state or len(st.session_state.abc_quiz_questions) != max_questions:
        def generate_abc_question():
            quiz_type = random.choice(["next", "missing"])
            idx = random.randint(0, 23)
            if quiz_type == "next":
                seq = letters[idx:idx+2]
                answer_letter = letters[idx+2]
                display_seq = seq + ["?"]
                prompt = f"What comes after {seq[1]}?"
            else:
                seq = [letters[idx], letters[idx+2]]
                answer_letter = letters[idx+1]
                display_seq = [seq[0], "?", seq[1]]
                prompt = f"What letter is missing between {seq[0]} and {seq[1]}?"
            return {
                'display_seq': display_seq,
                'answer_letter': answer_letter,
                'prompt': prompt,
                'user_input': '',
                'correct': None
            }
        st.session_state.abc_quiz_questions = [generate_abc_question() for _ in range(max_questions)]
        st.session_state.abc_quiz_submitted = False
    questions = st.session_state.abc_quiz_questions
    submitted = st.session_state.abc_quiz_submitted

    if not submitted:
        with st.form("abc_quiz_form_tab3"):
            for idx, current_q in enumerate(questions):
                st.write(f"### Question {idx+1} of {max_questions}")
                st.write("### ", "  ".join(current_q['display_seq']))
                st.markdown(f"<div style='font-size:36px; font-weight:bold; margin-top:10px; margin-bottom:10px;'>{current_q['prompt']}</div>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, ltr in enumerate(current_q['display_seq']):
                    if ltr != "?":
                        fruit_name = get_fruit_name(ltr)
                        cols[i].image(get_letter_image(ltr), caption=f"{ltr} - {fruit_name}", width='stretch')
                    else:
                        cols[i].markdown("<h2 style='text-align:center;'>?</h2>", unsafe_allow_html=True)
                user_input = st.text_input("Your Answer", max_chars=1, key=f"abc_seq_input_{idx}").upper()
                questions[idx]['user_input'] = user_input
            submitted_form = st.form_submit_button("Submit Quiz")
            if submitted_form:
                for q in questions:
                    q['correct'] = (q['user_input'] == q['answer_letter'])
                st.session_state.abc_quiz_questions = questions
                st.session_state.abc_quiz_submitted = True
    if submitted:
        st.header("Quiz Results")
        correct_count = sum(1 for q in questions if q.get('correct'))
        st.markdown(f"<h2 style='color:green;'>You got {correct_count} out of {max_questions} correct!</h2>", unsafe_allow_html=True)
        for i, q in enumerate(questions):
            fruit_name = get_fruit_name(q['answer_letter'])
            st.write(f"Q{i+1}: {' '.join(q['display_seq'])}")
            st.write(f"Your answer: {q['user_input']} | Correct answer: {q['answer_letter']} - {fruit_name}")
            if q.get('correct'):
                st.success("Correct!")
            else:
                st.error("Wrong!")
        if st.button("Restart Quiz", key="abc_seq_restart"):
            st.session_state.abc_quiz_questions = []
            st.session_state.abc_quiz_submitted = False

with tab4:
    st.header("Number Comparison Quiz")
    import random
    from PIL import Image, ImageDraw, ImageFont
    import io
    # Generate 5 unique random pairs for the session (isolate state for this tab)
    # Handle restart flag
    if st.session_state.get('numquiz_restart', False):
        for k in ['numquiz_pairs', 'numquiz_answers', 'numquiz_submitted', 'numquiz_key_prefix']:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.numquiz_restart = False
    if 'numquiz_pairs' not in st.session_state:
        pairs = set()
        while len(pairs) < 5:
            a, b = random.sample(range(1, 101), 2)
            pair = tuple(sorted((a, b)))
            pairs.add(pair)
        quiz_pairs = []
        for pair in list(pairs):
            a, b = pair
            if random.choice([True, False]):
                quiz_pairs.append((a, b))
            else:
                quiz_pairs.append((b, a))
        st.session_state.numquiz_pairs = quiz_pairs
        st.session_state.numquiz_answers = [""] * 5
        st.session_state.numquiz_submitted = False
    quiz_pairs = st.session_state.numquiz_pairs
    answers = st.session_state.numquiz_answers
    # Always use session state for submission
    submitted = st.session_state.get('numquiz_submitted', False)

    def numquiz_draw_circle_number(num):
        img = Image.new('RGBA', (120, 120), color='white')
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 112, 112), outline='black', width=6)
        try:
            font = ImageFont.truetype("arialbd.ttf", 36)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            except:
                font = ImageFont.load_default()
        bbox = font.getbbox(str(num)) if hasattr(font, 'getbbox') else draw.textbbox((0,0), str(num), font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((120-w)/2, (120-h)/2), str(num), fill='blue', font=font)
        return img

    def numquiz_add_tick_to_image(img):
        draw = ImageDraw.Draw(img)
        tick = [(80, 90), (100, 110), (115, 70)]
        draw.line(tick[:2], fill='green', width=6)
        draw.line(tick[1:], fill='green', width=6)
        return img

    # Use a unique prefix for this session to avoid duplicate keys
    import uuid
    if 'numquiz_key_prefix' not in st.session_state:
        st.session_state['numquiz_key_prefix'] = str(uuid.uuid4())[:8]
    key_prefix = st.session_state['numquiz_key_prefix']

    if not submitted:
        for i, (a, b) in enumerate(quiz_pairs):
            st.markdown(f"### Question {i+1}")
            cols = st.columns(2)
            btn_left = btn_right = False
            with cols[0]:
                img_a = numquiz_draw_circle_number(a)
                if answers[i] == "Left":
                    img_a = numquiz_add_tick_to_image(img_a)
                buf_a = io.BytesIO()
                img_a.save(buf_a, format='PNG')
                st.image(buf_a.getvalue(), width='content')
                btn_left = st.button(" ", key=f"numquiz_{key_prefix}_btn_left_{i}", help=f"Select {a}", disabled=answers[i]=="Left")
            with cols[1]:
                img_b = numquiz_draw_circle_number(b)
                if answers[i] == "Right":
                    img_b = numquiz_add_tick_to_image(img_b)
                buf_b = io.BytesIO()
                img_b.save(buf_b, format='PNG')
                st.image(buf_b.getvalue(), width='content')
                btn_right = st.button(" ", key=f"numquiz_{key_prefix}_btn_right_{i}", help=f"Select {b}", disabled=answers[i]=="Right")
            # Make answer selection atomic: only one click needed
            if btn_left and answers[i] != "Left":
                answers[i] = "Left"
                st.session_state.numquiz_answers = answers.copy()
            if btn_right and answers[i] != "Right":
                answers[i] = "Right"
                st.session_state.numquiz_answers = answers.copy()
            if answers[i] == "Left":
                cols[0].success("Selected")
            elif answers[i] == "Right":
                cols[1].success("Selected")
        # Always show submit button, enable only if all answered
        all_answered = all(ans in ("Left", "Right") for ans in answers)
        submit_pressed = st.button(
            "Submit Quiz",
            key="numquiz_submit_btn",
            disabled=not all_answered,
            help="Answer all questions to enable submission."
        )
        # Only process submission if all answered and button was pressed
        if all_answered and submit_pressed:
            st.session_state.numquiz_submitted = True
    if st.session_state.get('numquiz_submitted', False):
        # Calculate score
        score = 0
        for i, (a, b) in enumerate(quiz_pairs):
            correct = "Left" if a > b else "Right"
            if answers[i] == correct:
                score += 1
        st.success(f"You got {score} out of {len(quiz_pairs)} correct!")
        # Show correct answers for each question
        for i, (a, b) in enumerate(quiz_pairs):
            correct = "Left" if a > b else "Right"
            user = answers[i]
            st.markdown(f"**Q{i+1}: {a} vs {b}**")
            st.write(f"Your answer: {user} | Correct answer: {correct}")
            if user == correct:
                st.success("Correct!")
            else:
                st.error("Wrong!")
        if st.button("Restart Number Quiz", key="numquiz_restart_btn"):
            st.session_state.numquiz_restart = True

with tab1:
    st.header("Take the Quiz!")
    # Use session state to persist quiz and answers
    if 'quiz' not in st.session_state or st.session_state.get('reset_quiz', False):
        st.session_state.quiz = generate_quiz(5)
        st.session_state.answers = [None] * 5
        st.session_state.submitted = False
        st.session_state.reset_quiz = False

    quiz = st.session_state.quiz
    answers = st.session_state.answers
    submitted = st.session_state.submitted

    tick_svg = """
    <svg width='40' height='40' viewBox='0 0 24 24' fill='none' stroke='green' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 10 18 4 12'></polyline></svg>
    """
    for i, (question, options, answer) in enumerate(quiz):
        st.markdown(f"**Q{i+1}: {question}**")
        cols = st.columns(len(options))
        selected = answers[i]
        for j, opt in enumerate(options):
            img = get_preloaded_image(opt)
            btn_key = f"imgbtn_{i}_{j}"
            # Overlay tick if selected
            show_tick = (selected == opt)
            if not submitted:
                if cols[j].button(" ", key=btn_key, help=f"Select {opt}"):
                    answers[i] = opt
                    st.session_state.answers = answers
                    st.rerun()
            border_color = "green" if submitted and opt == answer else ("red" if submitted and selected == opt else None)
            cols[j].image(img, width='stretch')
            if show_tick:
                cols[j].markdown(f"<div style='position:relative; top:-45px; left:0;'>{tick_svg}</div>", unsafe_allow_html=True)
            if border_color:
                cols[j].markdown(f'<div style="border: 3px solid {border_color}; width: 100%; height: 5px;"></div>', unsafe_allow_html=True)
        if selected:
            st.markdown(f"Selected answer: :blue[{selected}]")
        else:
            st.markdown(":grey_question: No answer selected yet.")
        st.markdown("---")

    if not submitted:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True
            submitted = True


    if submitted:
        score = sum([(a == quiz[i][2]) for i, a in enumerate(answers) if a is not None])
        st.markdown(f"<h2 style='color:green; font-weight:bold;'>You got {score} out of {len(quiz)} correct!</h2>", unsafe_allow_html=True)
        # Show winner image and flashing message if score > 3 and user uploaded image
        if score > 3 and st.session_state.get('user_image'):
            import base64
            st.markdown("<h3 style='color:gold;'>You are the winner!</h3>", unsafe_allow_html=True)
            b64_img = base64.b64encode(st.session_state['user_image']).decode()
            st.markdown("""
                <style>
                @keyframes borderflash {
                    0% { border-color: magenta; }
                    100% { border-color: gold; }
                }
                .winner-img {
                    border: 6px solid magenta;
                    animation: borderflash 1s infinite alternate;
                    display: inline-block;
                    margin: 10px;
                    border-radius: 10px;
                }
                @keyframes flash {
                    0% { color: magenta; }
                    100% { color: gold; }
                }
                .winner-msg {
                    animation: flash 1s infinite alternate;
                    font-size: 2em;
                    font-weight: bold;
                }
                </style>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='winner-img'><img src='data:image/png;base64,{b64_img}' width='200'></div>", unsafe_allow_html=True)
            st.markdown("<div class='winner-msg'>You are the winner!</div>", unsafe_allow_html=True)
        if st.button("More Questions?"):
            st.session_state.reset_quiz = True
            st.session_state.submitted = False
            st.rerun()

with tab2:
    st.header("Animal List")
    animals = get_animal_list()
    for animal in animals:
        st.write(f"- {animal}")
