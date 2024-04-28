import streamlit as st
from generate_questions import generate_questions
from evaluate_student import evaluate_student_wrapper, check_id, load_data
from model_setup import model_setup
model, tokenizer = model_setup()
st.title("Personalized Review Questions")
student_id = st.text_input("Enter a valid student ID")
df = load_data()
if st.button("Generate Questions"):
    if student_id:
        try:
            check_id(df, student_id)
        except ValueError as e:
            st.error("Invalid student ID. Please enter a valid student ID.")
    topics, level = evaluate_student_wrapper(student_id, df)
    st.write("The sections you should review are {}, {}, and {}".format(topics[0], topics[1], topics[2]))
    # questions, answers = generate_questions(topics, level, model, tokenizer)
    questions = ["hi"] * 15
    answers = ["hi"] * 15 
    st.header(f'Topic 1: {topics[0]}')
    for i in range(0, 5):
        st.write(questions[i])
    st.header(f'Topic 2: {topics[1]}')
    for i in range(5, 10):
        st.write(questions[i])
    st.header(f'Topic 3: {topics[2]}')
    for i in range(10, 15):
        st.write(questions[i])