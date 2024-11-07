import streamlit as st
import requests
import random
import time
from io import BytesIO
import os

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #282c34;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 36px;
        text-align: center;
        color: #ff6f61;
        font-weight: bold;
    }
    .question {
        font-size: 24px;
        text-align: center;
        color: #f5a623;
        margin: 20px;
    }
    .button {
        background-color: #ff6f61;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #ff4a39;
    }
    .score {
        font-size: 28px;
        text-align: center;
        color: #f5a623;
    }
    .leaderboard {
        font-size: 22px;
        color: #f5a623;
        margin: 20px;
    }
    .countdown {
        font-size: 18px;
        text-align: center;
        color: #ff6f61;
    }
    </style>
""", unsafe_allow_html=True)

# Function to fetch trivia question
def get_trivia_question(difficulty):
    url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty.lower()}&type=multiple"
    response = requests.get(url)
    if response.status_code != 200 or not response.json()['results']:
        return None
    data = response.json()['results'][0]
    question = data['question']
    correct_answer = data['correct_answer']
    choices = data['incorrect_answers']
    choices.append(correct_answer)
    random.shuffle(choices)
    return question, choices, correct_answer

# Function to play sound effects if the file exists
def play_sound(file_path):
    if os.path.exists(file_path):
        audio_file = open(file_path, 'rb').read()
        audio_bytes = BytesIO(audio_file)
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.write(f"Sound file '{file_path}' not found.")

# Display choices with hover effects and unique keys
def display_choices_with_emojis(choices, question_number):
    emoji_choices = ['🔴', '🟢', '🟡', '🔵']
    button_columns = st.columns(2)  # Create 2 columns for choices
    for idx, choice in enumerate(choices):
        with button_columns[idx % 2]:  # Alternate buttons between two columns
            # Assign a unique key to each button using question number and index
            if st.button(f"{emoji_choices[idx]} {choice}", key=f"choice_{question_number}_{idx}"):
                return choice
    return None

# Initialize session state variables
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1
    st.session_state.score = 0
    st.session_state.time_left = 30
    st.session_state.correct_answer = None
    st.session_state.use_sound = True  # Default to using sound

# Timer countdown logic
if st.session_state.time_left > 0:
    st.session_state.time_left -= 1
    time.sleep(1)

# Display title and instructions
st.title("AI-Powered Virtual Trivia Game")
st.write("""
Welcome to the Trivia Game! 
- Choose your difficulty level and try to answer the questions as fast as you can.
- You will get points for correct answers. 
- Your score will be displayed at the end of the game.
""")

# Toggle sound effects
st.session_state.use_sound = st.checkbox("Enable Sound Effects", value=True)

# Choose difficulty level
difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])

# Load a new question
if 'question' not in st.session_state or st.button("Next Question"):
    question_data = get_trivia_question(difficulty)
    if question_data is not None:
        st.session_state.question, st.session_state.choices, st.session_state.correct_answer = question_data
        st.session_state.time_left = 30  # Reset timer for each question

# Display question and countdown timer
st.subheader(f"Question {st.session_state.question_number}")
st.markdown(f"<div class='question'>{st.session_state.question}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='countdown'>Time Left: {st.session_state.time_left} seconds</div>", unsafe_allow_html=True)

# Display answer choices with unique keys for each question and choice
user_answer = display_choices_with_emojis(st.session_state.choices, st.session_state.question_number)

# Check the answer and update score
if user_answer:
    if user_answer == st.session_state.correct_answer:
        st.session_state.score += 1
        if st.session_state.use_sound:
            play_sound('correct-156911.mp3')
        st.write("Correct!")
    else:
        if st.session_state.use_sound:
            play_sound('wrong-answer-129254.mp3')
        st.write(f"Wrong! The correct answer was {st.session_state.correct_answer}.")
    st.session_state.question_number += 1

# Display score and next question button
st.subheader(f"Your Current Score: {st.session_state.score}")
if st.session_state.question_number > 5:  # End the game after 5 questions
    st.write("Game Over!")
    st.markdown(f"<div class='score'>Final Score: {st.session_state.score}/5</div>", unsafe_allow_html=True)
else:
    if st.button("Next Question", key="next_question"):
        st.session_state.time_left = 30  # Reset timer for next question
