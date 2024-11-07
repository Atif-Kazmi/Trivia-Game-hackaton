import streamlit as st
import requests
import random
import time
from io import BytesIO

# Add Custom CSS for styling
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
    .progress {
        height: 20px;
        background-color: #ff6f61;
    }
    .countdown {
        font-size: 18px;
        text-align: center;
        color: #ff6f61;
    }
    </style>
""", unsafe_allow_html=True)

# Sound Effect Function
def play_sound(file_path):
    audio_file = open(file_path, 'rb').read()
    audio_bytes = BytesIO(audio_file)
    st.audio(audio_bytes, format="audio/wav")

# Fetch trivia question from OTDB
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

# Timer animation
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        st.markdown(f"<div class='countdown'>Time left: {i}s</div>", unsafe_allow_html=True)
        time.sleep(1)
        st.experimental_rerun()  # Use this to force a re-run each second

# Display choices with hover effects
def display_choices_with_emojis(choices):
    emoji_choices = ['🔴', '🟢', '🟡', '🔵']
    button_columns = st.columns(2)  # Create 2 columns for choices
    for idx, choice in enumerate(choices):
        with button_columns[idx % 2]:  # Alternate buttons between two columns
            if st.button(f"{emoji_choices[idx]} {choice}", key=idx):
                return choice
    return None

# Add Leaderboard with Progress Bar
def leaderboard_with_progress_bar(leaderboard):
    leaderboard_sorted = sorted(leaderboard, reverse=True)
    for i, score in enumerate(leaderboard_sorted):
        st.markdown(f"<div class='leaderboard'>{i+1}. Score: {score}</div>", unsafe_allow_html=True)
        progress = score / max(leaderboard_sorted) * 100
        st.progress(progress)

# Start the game
def start_game():
    st.title("AI-Powered Virtual Trivia Game")
    st.write("""
    Welcome to the Trivia Game! 
    - Choose your difficulty level and try to answer the questions as fast as you can.
    - You will get points for correct answers. 
    - Your score will be displayed at the end of the game.
    """)

    # Choose difficulty level
    difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])
    
    score = 0
    num_questions = 5
    question_number = 1
    leaderboard = []

    while question_number <= num_questions:
        st.subheader(f"Question {question_number}")
        
        question_data = get_trivia_question(difficulty)
        if question_data is None:
            st.write("Error fetching question, please try again.")
            break
        
        question, choices, correct_answer = question_data
        st.markdown(f"<div class='question'>{question}</div>", unsafe_allow_html=True)
        
        # Show timer and start countdown
        countdown_timer(30)
        
        user_answer = display_choices_with_emojis(choices)
        
        # Play sound for correct or wrong answer
        if user_answer == correct_answer:
            play_sound('correct_answer.wav')
            score += 1
            st.write("Correct!")
        else:
            play_sound('wrong_answer.wav')
            st.write(f"Wrong! The correct answer was {correct_answer}.")
        
        question_number += 1

    # Add score to leaderboard
    leaderboard.append(score)
    
    st.subheader(f"Game Over! Your Score: {score}/{num_questions}")
    
    # Show dynamic leaderboard
    leaderboard_with_progress_bar(leaderboard)

    # Display game results
    st.write("Game Over!")
    st.markdown(f"<div class='score'>Your Final Score: {score}/{num_questions}</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    start_game()
