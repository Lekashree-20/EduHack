import streamlit as st
import requests
import json
import plotly.express as px

# Function to fetch MCQ questions from the API
def fetch_questions(subject_name):
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='
    }
    data = {
        "promptId": "4e51e8b3-f6eb-41bb-8f0f-e92a910e7caf",
        "promptVersionId": "7e014386-e0ff-43cd-89de-bdff820e2f3d",
        "replacements": {
            "subject": subject_name
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return None

# Function to parse questions, options, and answers
def parse_questions(content):
    questions_data = json.loads(content)  # Safely parse JSON content
    questions = questions_data['questions']
    return questions

# Streamlit App
def main():
    st.title("MCQ Test")

    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    subject_name = st.text_input("Enter the subject name:")

    if st.button("Fetch Questions"):
        if subject_name:
            questions_content = fetch_questions(subject_name)
            if questions_content:
                st.session_state.questions = parse_questions(questions_content)
                total_questions = len(st.session_state.questions)

                if not st.session_state.user_answers:
                    st.session_state.user_answers = {i: None for i in range(1, total_questions + 1)}

    if st.session_state.questions:
        total_questions = len(st.session_state.questions)
        for i, question in enumerate(st.session_state.questions, 1):
            st.subheader(f"Question {i}/{total_questions}:")
            st.write(question['question'])
            options = question['options']
            selected_option = st.radio(f"Options for Question {i}:", options, 
                                       key=f"question_{i}", 
                                       index=options.index(st.session_state.user_answers[i]) if st.session_state.user_answers[i] is not None else 0)
            st.session_state.user_answers[i] = selected_option

        if st.button("Submit Answers"):
            st.session_state.score = sum(1 for i in range(1, total_questions + 1) if st.session_state.user_answers[i] == st.session_state.questions[i - 1]['answer'])
            st.write("Your Score:", st.session_state.score, "/", total_questions)

            # Progress bar visualization
            score_percentage = st.session_state.score / total_questions
            st.progress(score_percentage)

            # Pie chart visualization
            fig = px.pie(
                names=["Correct", "Incorrect"],
                values=[st.session_state.score, total_questions - st.session_state.score],
                title="Score Distribution"
            )
            st.plotly_chart(fig)
            
            st.write("Thanks for taking the test!")

if __name__ == "__main__":
    main()
