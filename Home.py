import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="EduPath")
st.title("EduPath")

# Add image
st.image("Images\education-removebg-preview.png", use_column_width=True)  # Adjust path to your image file

st.header("Objective:")
st.markdown('''The primary goal of our EduPath project is to revolutionize the education experience by integrating advanced artificial intelligence (AI) capabilities.''')
st.header("Syllabus Generation and Content Delivery:")
st.markdown('''Description:\n\nEduPath harnesses AI to automatically generate a comprehensive syllabus based on current trends for any subject the user specifies. This feature ensures that learners have access to the most relevant and up-to-date information in their field of study.\n
Functionality:\n''')
bullet_points = [
"Users input the subject name.",
"The AI generates a syllabus that reflects the latest developments and trends in the specified subject.",
"The generated syllabus includes subtopics.",
"Users can click on any subtopic to receive detailed content related to it.",
"This content is fetched automatically using Hyperleap AI, providing users with accurate and relevant information."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.header("Interactive Test Session:")
st.markdown("Description:")
st.markdown('''EduPath includes an interactive test session that assesses the user's knowledge based on the content they have learned. This feature ensures that learners can track their progress and identify areas for improvement.''')
st.markdown("Functionality:")
bullet_points = [
"Based on the content delivered, the system generates multiple-choice questions (MCQs).",
"These questions are designed to test the user's understanding of the material.",
"Users take the test, and their responses are evaluated in real-time.",
"The system provides immediate feedback and scores.",
"The results are visualized to show the user's progress and areas needing improvement.",
"This visual feedback helps users understand their learning journey and focus on weaker areas."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.header("PDF Interaction and Q&A:")
st.markdown("Description:")
st.markdown('''EduPath offers a feature where users can upload PDF documents and ask questions related to the content within them. The AI, powered by Google's Gemini, provides accurate answers, enhancing the user's understanding and engagement with the material.''')
st.markdown("Functionality:")
bullet_points = [
"Users can upload PDF files containing educational material.",
"Users ask questions related to the content in the PDF.",
"The AI processes these questions and retrieves relevant information from the PDF to provide accurate answers.",
"This feature supports deep engagement with course materials, allowing users to clarify doubts and gain a better understanding of the content."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.markdown('''Conclusion:\n\nEduPath combines syllabus generation, content delivery, interactive testing, and intelligent document interaction to provide a comprehensive educational platform. By leveraging AI, EduPath ensures that learners have access to the most relevant information, can assess their knowledge effectively, and engage deeply with their study materials.''')
