import st_app as st
from generate_questions import generate_questions
from evaluate_student import evaluate_student_wrapper, check_id
from model_setup import model_setup
model, tokenizer = model_setup()
st.title("Personalized Review Questions")
student_id = st.text_input("Enter a valid student ID")
if student_id:
    try:
        check_id(df, student_id)
    except ValueError as e:
        st.error("Invalid student ID. Please enter a valid student ID.")
if st.button("Generate Questions"):
    topics, level = evaluate_student_wrapper(student_id)
    questions = generate_questions(topics, level, model, tokenizer)
    st.write(questions)