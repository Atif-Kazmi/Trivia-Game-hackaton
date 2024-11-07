import streamlit as st
import requests
import random
import time

# Function to fetch a trivia question from the Open Trivia Database (OTDB)
def get_trivia_question(difficulty):
    url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty.lower()}&type=multiple"
    response = requests.get(url)
    
    # Handle if no questions are returned or there was an error
    if response.status_code != 200 or not response.json()['results']:
        return None
    
    data = response.json()['results'][0]
    
    # Extract question and answers
    question = data['question']
    correct_answer = data['correct_answer']
    choices = data['incorrect_answers']
    choices.append(correct_answer)
    random.shuffle(choices)  # Shuffle the choices to randomize the answer positions
    
    return question, choices, correct_answer

# Function to start the game
def start_game():
    # Display title and instructions
    st.title("AI-Powered Virtual Trivia Game")
    st.write("""
    Welcome to the Trivia Game! 
    - Choose your difficulty level and try to answer the questions as fast as you can.
    - You will get points for correct answers. 
    - Your score will be displayed at the end of the game.
    """)

    # Choose difficulty level
    difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])
    
    # Initialize variables for the game
    score = 0
    num_questions = 5  # Number of questions to ask
    question_number = 1
    leaderboard = []
    
    # Game loop
    while question_number <= num_questions:
        st.subheader(f"Question {question_number}")
        
        # Get trivia question from OTDB
        question_data = get_trivia_question(difficulty)
        if question_data is None:
            st.write("Error fetching question, please try again.")
            break
        
        question, choices, correct_answer = question_data
        st.write(question)
        
        # Display multiple choice options
        option_a, option_b, option_c, option_d = choices
        user_answer = st.radio("Your Answer", [option_a, option_b, option_c, option_d])
        
        # Timer (30 seconds per question)
        timer = 30
        with st.empty():
            for t in range(timer, 0, -1):
                st.write(f"Time left: {t} seconds")
                time.sleep(1)
        
        # Check if the answer is correct
        if user_answer == correct_answer:
            score += 1
            st.write("Correct!")
        else:
            st.write(f"Wrong! The correct answer was {correct_answer}.")
        
        question_number += 1
    
    # Display final score
    st.subheader(f"Game Over! Your Score: {score}/{num_questions}")
    
    # Leaderboard (temporary list for the hackathon, can be replaced with a database)
    leaderboard.append(score)
    
    # Display leaderboard
    leaderboard.sort(reverse=True)
    st.write("Leaderboard:")
    for i, score in enumerate(leaderboard, 1):
        st.write(f"{i}. Score: {score}")

# Streamlit app layout
if __name__ == "__main__":
    start_game()
