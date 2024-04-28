import pandas as pd
import streamlit as st

def evaluate_student_by_first_attempt(df, student_id):
    student_data = df[df['student_id'] == student_id]
    student_data = student_data[student_data['attempt'] == 1]
    if(student_data.shape[0] < 10):
        print("Student Must Answer More Questions")
        return None

    topics_list = (student_data.groupby('page_topic')['points_earned'].sum() /
                        student_data.groupby('page_topic')['points_possible'].sum()).sort_values()

    return 1 - topics_list

def evaluate_student_by_chapter(df, student_id, chapter):
    df = df[df['chapter'] == chapter]
    return evaluate_student_wrapper(df, student_id)

def evaluate_student_by_unanswered_questions(df, student_id):
    student_data = df[df['student_id'] == student_id]
    max_attempts = student_data.groupby('prompt')['attempt'].max().reset_index()
    max_attempts.rename(columns={'attempt': 'Max_Attempts'}, inplace=True)
    student_data = pd.merge(student_data, max_attempts, on = 'prompt', how = "left")
    student_data['unanswered'] = ((student_data['Max_Attempts'] == student_data['attempt']) & 
                (student_data['points_earned'] != student_data['points_possible'])).astype(int)
    topics_list = student_data.groupby('page_topic')['unanswered'].mean().sort_values(ascending=False) # actually gets the proportion
    return topics_list

# def evaluate_student_by_attempts_til_correct(df, student_id):
#     '''

#     :param df:
#     :param topics:
#     :return topics_list, level:
#     '''

#     # sorry for ugly code :( all good lol

#     stud = df[df["student_id"] == student_id]

#     if (stud["page_topic"].nunique() < 10):
#         print("Student Must Answer More Questions")
#         return None

#     stud["correct"] = (stud["points_earned"] == stud["points_possible"])
#     correct_questions = stud[stud["correct"]]
#     correct_questions = correct_questions[["page_topic", "item_id", "prompt", "attempt"]]

#     min_attempts = correct_questions.groupby(["item_id", "prompt", "page_topic"])["attempt"].min()
#     average_attempts_by_topic = min_attempts.reset_index().groupby(["page_topic"])["attempt"].mean()
#     topics_list = average_attempts_by_topic.sort_values(ascending=False)
#     return topics_list

def evaluate_student_topics(first_attempt, unanswered):
    
    # Perform min-max scaling on all results
    first_attempt = (first_attempt - first_attempt.min()) / (first_attempt.max() - first_attempt.min())
    # first_success = (first_success - first_success.min()) / (first_success.max() - first_success.min())
    unanswered = (unanswered - unanswered.min()) / (unanswered.max() - unanswered.min())
    
    combined = 0.6 * first_attempt + 0.4 * unanswered
    
    return list(combined.sort_values(ascending = False).index[0:3])

def evaluate_student_wrapper(student_id, df):
    '''

    :return:
    '''
    # We will assume that the CSVs are in the Data folder
    #add argparse to get the student id and the evaluation method    

    
    first_attempt = evaluate_student_by_first_attempt(df, student_id)
    # first_success = evaluate_student_by_attempts_til_correct(df, student_id)
    unanswered = evaluate_student_by_unanswered_questions(df, student_id)
    
    worst_topics = evaluate_student_topics(first_attempt, unanswered)
    
    book = df[df['student_id'] == student_id]["book"].unique()[0]
    if (book == "College / Advanced Statistics and Data Science (ABCD)"):
        level = "advanced college"
    elif (book == "College / Statistics and Data Science (ABC)"):
        level = "college"
    else:
        level = "high school"
    return worst_topics, level

def check_id(df, student_id):
    '''

    :param df:
    :param student_id:
    :return:
    '''
    if student_id not in df["student_id"].unique():
        raise ValueError("Invalid student ID. Please enter a valid student ID.")
    else:
        return

@st.cache(allow_output_mutation=True)
def load_data():
    '''

    :return:
    '''
    df = pd.read_csv("Data/Full Data/scores.csv")
    return df
