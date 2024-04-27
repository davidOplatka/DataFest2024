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

    return topics_list



def evaluate_student_by_attempts_til_correct(df, student_id):
    '''

    :param df:
    :param topics:
    :return topics_list, level:
    '''

    # sorry for ugly code :( all good lol

    stud = df[df["student_id"] == student_id]

    if (stud["page_topic"].nunique() < 10):
        print("Student Must Answer More Questions")
        return None

    stud["correct"] = (stud["points_earned"] == stud["points_possible"])
    correct_questions = stud[stud["correct"]]
    correct_questions = correct_questions[["page_topic", "item_id", "prompt", "attempt"]]

    min_attempts = correct_questions.groupby(["item_id", "prompt", "page_topic"])["attempt"].min()
    average_attempts_by_topic = min_attempts.reset_index().groupby(["page_topic"])["attempt"].mean()
    topics_list = average_attempts_by_topic.sort_values(ascending=False)
    return topics_list

def evaluate_student_wrapper(studetnt_id):
    '''

    :return:
    '''
    # We will assume that the CSVs are in the Data folder
    #add argparse to get the student id and the evaluation method


    df = pd.read_csv("Data/Full Data/scores.csv")

    book = df[df['student_id'] == student_id]["book"].unique()[0]
    if (book == "College / Advanced Statistics and Data Science (ABCD)"):
        level = "advanced college"
    elif (book == "College / Statistics and Data Science (ABC)"):
        level = "college"
    else:
        level = "high school"
    return topics_list, level

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
def evaluate_student_wrapper(student_id, df):
    '''

    :return:
    '''
    # We will assume that the CSVs are in the Data folder
    #add argparse to get the student id and the evaluation method

    #TODO Pass the Df and the student_id to the function to get the topics and the level
