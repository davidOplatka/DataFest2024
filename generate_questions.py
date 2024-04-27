from model_setup import model_setup
from constants import PROMPT_FORMAT_STRING
import torch

def create_prompt(topic, student_level):
    '''
    Generate a prompt for the model to generate questions.
    :param topic: The topic of the questions.
    :param student_level: The level of the students.
    :return: A string prompt.
    '''
    return  {"role": "user", "content": PROMPT_FORMAT_STRING.format(topic, student_level)}



def generate_batch_prompt(topics, student_level):
    '''
    Generate a prompt for the model to generate questions in batch.
    :param topics: A list of topics of the questions.
    :param student_level: The level of the students.
    :return: A list of string prompts.
    '''
    prompt_list =[{"role": "system", "content": "You are a statistics teacher, you need to create a set of review questions for the given topic and student level"}]
    for topic in topics:
        prompt_list.append(create_prompt(topic, student_level))
    return prompt_list

def generate_questions(topics, student_level):
    '''
    Generate a set of review questions for the given topics and student level.
    :param topics: A list of topics of the questions.
    :param student_level: The level of the students.
    :return: A list of questions.
    '''
    model_pipeline = model_setup()
    prompts = generate_batch_prompt(topics, student_level)
    prompt = model_pipeline.tokenizer.apply_chat_template(
        prompts,
        tokenize=False,
        add_generation_prompt=True
    )

    terminators = [
        model_pipeline.tokenizer.eos_token_id,
        model_pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    with torch.no_grad():
        outputs = model_pipeline(
            prompt,
            max_new_tokens=512,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )

    #Extract the Answers from the generrated text
    answers = []
    questions = []
    for output in outputs:
        text = output["generated_text"]
        lines = text.splitlines()
        for line in lines:
            if line.startswith("ANSWER:"):
                answers.append(line)
            elif line.startswith("QUESTION:"):
                questions.append(line)
        question, answer = text.split("ANSWER:")
        questions.append(question)
        answers.append(answer)

    return questions, answers