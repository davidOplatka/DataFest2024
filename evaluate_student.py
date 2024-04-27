import pandas as pd
import argparse

def evaluate_student(student_id):
    '''

    :param student_id:
    :return:
    '''
    pass

def group_questions_by_topic(df, topics):
    '''

    :param df:
    :param topics:
    :return:
    '''
    pass

def main():
    '''

    :return:
    '''
    # We will assume that the CSVs are in the Data folder
    #add argparse to get the student id and the evaluation method
    parser = argparse.ArgumentParser()
    parser.add_argument("student_id", help="The student ID to evaluate")
    parser.add_argument("evaluation_method", help="The method to evaluate the student")
    args = parser.parse_args()
    student_id = args.student_id
    evaluation_method = args.evaluation_method

    df = pd.read_csv("Data/Full Data/updated_topics.csv")

    #TODO: Implement the functions to evaluate students using various heuristics