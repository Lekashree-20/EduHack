import os
import streamlit as st
import requests
import json
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize model for doubt clearing session
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

st.title("Academic Assistant")

# Function to fetch content data
def fetch_content_data(subtopic_name, subject_name):
    CONTENT_API_URL = 'https://api.hyperleap.ai/prompts'
    API_KEY = 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='

    payload = {
        "promptId": "f937db13-4d95-43f0-9e71-1dda1dc146ea",
        "promptVersionId": "2e58658d-e8ca-44ee-814e-29c4a81095be",
        "replacements": {
            "subtopic": subtopic_name,
            "subject": subject_name
        }
    }

    headers = {
        "accept": "application/json",
        "x-hl-api-key": API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(CONTENT_API_URL, data=json.dumps(payload), headers=headers)
    return response

# Text input for course name
name = st.text_input("Enter the course name:")

# Submit button
if st.button("Submit"):
    url = 'https://api.hyperleap.ai/prompts'
    api_key = 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='
    name_str = str(name)

    payload = {
        "promptId": "81590497-4e97-42e3-b8d7-901c65d24f1f",
        "promptVersionId": "989d1c23-1cb3-4092-ba9b-4fcd456fdd08",
        "replacements": {
            "subject": name_str
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': api_key
    }

    def fetch_course_data():
        response = requests.post(url, json=payload, headers=headers)
        return response

    res = fetch_course_data()

    if res.status_code == 200:
        course_data = json.loads(res.json()["choices"][0]["message"]["content"])
        st.session_state['course_data'] = course_data
        st.session_state['course_name'] = name_str

if 'course_data' in st.session_state:
    course_data = st.session_state['course_data']
    course_name = st.session_state['course_name']
    
    chapter_names = [chapter["chapterName"] for chapter in course_data[0]["chapters"]]
    selected_chapter_index = st.selectbox("Select a chapter:", range(len(chapter_names)), format_func=lambda x: chapter_names[x])
    selected_chapter = course_data[0]["chapters"][selected_chapter_index]

    st.write(f"Subtopics for {selected_chapter['chapterName']}:")

    for subtopic in selected_chapter["subTopics"]:
        if st.button(subtopic):
            res = fetch_content_data(subtopic, course_name)
            st.write("Response status code:", res.status_code)

            if res.status_code == 200:
                try:
                    content_str = res.content.decode('utf-8')
                    res_json = json.loads(content_str)
                    content_message = res_json["choices"][0]["message"]["content"]

                    st.header(subtopic)
                    st.write(content_message)

                    # Add TTS button
                    escaped_content_message = content_message.replace('`', '\\`').replace('\n', '\\n')
                    components.html(f"""
                    <!DOCTYPE html>
                    <html>
                    <head></head>
                    <body>
                        <button onclick="speak()">Listen to this content</button>
                        <script>
                        if ('speechSynthesis' in window) {{
                            function speak() {{
                                var msg = new SpeechSynthesisUtterance();
                                msg.text = `{escaped_content_message}`;  // Ensure backticks are escaped
                                msg.lang = 'en-US';
                                msg.rate = 1;
                                msg.pitch = 1;
                                msg.volume = 1;
                                window.speechSynthesis.speak(msg);
                            }}
                        }} else {{
                            console.log('Your browser does not support text-to-speech.');
                        }}
                        </script>
                    </body>
                    </html>
                    """, height=100)
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Failed to parse content data: {str(e)}")
            else:
                st.error(f"Failed to fetch content data. Status code: {res.status_code}")

# Get user question from input
user_question = st.text_input("Ask your academic question:")

# Generate response based on user input
if st.button("Get Answer"):
    if user_question:
        if 'course_data' in st.session_state:
            course_data = st.session_state['course_data']
            course_name = st.session_state['course_name']
            context = ""

            # Construct context from course content
            for chapter in course_data[0]["chapters"]:
                for subtopic in chapter["subTopics"]:
                    context += subtopic + ". "
            
            # Append user's question to context
            context += user_question

            # Create prompt template
            prompt = ChatPromptTemplate.from_template(
                f"As a tutor, your role is to address the user's academic inquiries exclusively. Respond to their questions pertaining to studies and refrain from engaging in topics unrelated to academics. Interact with the user and impart knowledge accordingly. Remember, you should not answer any questions which are non-academic. User question: {context}"
            )
            
            # Define output parser
            output_parser = StrOutputParser()
            
            # Define the chain
            chain = prompt | model | output_parser
            
            # Invoke the chain
            result = chain.invoke({})
            
            # Display the generated response
            st.markdown(result)
        else:
            st.error("Please select a course and its content first.")
    else:
        st.error
