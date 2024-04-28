import streamlit as st
from generate_questions import generate_questions
from evaluate_student import evaluate_student_wrapper, check_id, load_data
from model_setup import model_setup

st.title("Personalized Review Questions")
student_id = st.text_input("Enter a valid student ID")
df = load_data()

# Check if 'model' and 'tokenizer' are already in the session state
if 'model' not in st.session_state or 'tokenizer' not in st.session_state:
    st.session_state['model'], st.session_state['tokenizer'] = model_setup()

flag = False
with st.form(key='generate_questions_form'):
    submit_button = st.form_submit_button(label='Generate Questions')
    if student_id:
        try:
            check_id(df, student_id)
        except ValueError as e:
            st.error("Invalid student ID. Please enter a valid student ID.")
    st.session_state["topics"], level = evaluate_student_wrapper(student_id, df)
    st.write("The sections you should review are {}, {}, and {}".format(st.session_state["topics"][0],st.session_state["topics"][1],st.session_state["topics"][2]))
    # st.session_state['questions'], st.session_state['answers'] = generate_questions(st.session_state["topics"], level, st.session_state['model'], st.session_state['tokenizer'])
    st.session_state['questions'] = ['hi'] * 15
    st.session_state['answers'] = ['hi'] * 15
    flag = True

if flag == True: 
    for topic_index in range(3):
        st.header(f'Topic {topic_index+1}: {st.session_state["topics"][topic_index]}')
        for i in range(topic_index*5, (topic_index+1)*5):
            if f'question_{i}' not in st.session_state:
                st.session_state[f'question_{i}'] = st.session_state['questions'][i]
                st.session_state[f'answer_{i}'] = False

            if st.session_state[f'answer_{i}']:
                st.write(st.session_state['answers'][i])
            else:
                st.write(st.session_state[f'question_{i}'])
                if st.checkbox(f'Show Answer for Question {i+1}'):
                    st.session_state[f'answer_{i}'] = True