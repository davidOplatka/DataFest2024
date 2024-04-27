import pandas as pd
import argparse

def evaluate_student_by_attempts_til_correct(df, student_id):
    '''

    :param df:
    :param topics:
    :return topics_list, level:
    '''

    # sorry for ugly code :( all good lol

    df["correct"] = (df["points_earned"] == df["points_possible"])
    topic_counts = df.groupby("student_id")["page_topic"].nunique()
    bad_studs = topic_counts[topic_counts < 10].index
    good_studs = df[~(df["student_id"].isin(bad_studs))].reset_index(drop=True)
    good_studs_correct = good_studs[good_studs["correct"]]
    good_studs_correct = good_studs_correct[["student_id", "book", "page_topic", "item_id", "prompt", "attempt"]]
    min_attempts = good_studs_correct.groupby(["student_id", "item_id", "prompt", "page_topic"])["attempt"].min()
    student_average_attempts_by_topic = min_attempts.reset_index().groupby(["student_id", "page_topic"])["attempt"].mean().reset_index()
    student_data = student_average_attempts_by_topic[student_average_attempts_by_topic['student_id'] == student_id]
    topics_list = list(student_data.sort_values(by="attempt", ascending=False)["page_topic"].iloc[0:3])
    book = df[df['student_id'] == student_id]["book"].unique()[0]
    if (book == "College / Advanced Statistics and Data Science (ABCD)"):
        level = "advanced college"
    elif (book == "College / Statistics and Data Science (ABC)"):
        level = "college"
    else:
        level = "high school"
    return topics_list, level

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

    df = pd.read_csv("Data/Full Data/scores.csv")

    #TODO: Implement the functions to evaluate students using various heuristics