
import streamlit as st

from animals import get_animal_list
from quiz import generate_quiz
from image_fetcher import get_animal_image
from PIL import Image
from email_utils import generate_code, send_verification_email
import re
import time


st.title("Animal Quiz App")


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

if not st.session_state.quiz_started:
    st.header("Enter your name and email to start the quiz")
    user_name = st.text_input("User Name", value=st.session_state.user_name, key="user_name_input")
    user_email = st.text_input("Email", value=st.session_state.user_email, key="user_email_input")
    if not st.session_state.email_verified:
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        sender_email = "quizmasterzenz@gmail.com"
        sender_password = st.text_input("Sender App Password", value="", type="password", key="sender_password")
        if st.button("Send Verification Code"):
            if user_name.strip() == '' or user_email.strip() == '' or sender_password.strip() == '':
                st.warning("All fields are mandatory.")
            elif not is_valid_email(user_email):
                st.warning("Please enter a valid email address.")
            else:
                code = generate_code()
                st.session_state.verification_code = code
                st.session_state.user_name = user_name
                st.session_state.user_email = user_email
                st.session_state.code_sent_time = time.time()
                try:
                    send_verification_email(user_email, code, smtp_server, smtp_port, sender_email, sender_password)
                    st.success(f"Verification code sent to {user_email}. Please check your email.")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")
        if st.session_state.verification_code:
            code_input = st.text_input("Enter the code sent to your email:", key="code_input")
            if st.button("Verify Code"):
                now = time.time()
                if now - st.session_state.code_sent_time > 60:
                    st.warning("Code expired. Please request a new code.")
                    st.session_state.verification_code = ''
                elif code_input == st.session_state.verification_code:
                    st.session_state.email_verified = True
                    st.success("Email verified! You can now start the quiz.")
                else:
                    st.error("Invalid code. Please try again.")
        st.stop()
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.rerun()

# Show animal list
tab1, tab2 = st.tabs(["Quiz", "Animals"])




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
            img = get_animal_image(opt)
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
        if st.button("More Questions?"):
            st.session_state.reset_quiz = True
            st.session_state.submitted = False
            st.rerun()

with tab2:
    st.header("Animal List")
    animals = get_animal_list()
    for animal in animals:
        st.write(f"- {animal}")
