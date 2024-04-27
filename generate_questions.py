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
    message_list = []
    for topic in topics:
        prompt_list =[{"role": "system", "content": "You are a statistics teacher, you need to create a set of review questions for the given topic and student level"}]
        prompt_list.append(create_prompt(topic, student_level))
        message_list.append(prompt_list)

    return message_list
def generate_questions(topics, student_level, model, tokenizer):
    '''
    Generate a set of review questions for the given topics and student level.
    :param topics: A list of topics of the questions.
    :param student_level: The level of the students.
    :return: A list of questions.
    '''

    messages = generate_batch_prompt(topics, student_level)
    print(messages)
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        padding=True,
        tokenize=True
    )

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            max_new_tokens=512,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
    #Extract the Answers from the generrated text
    decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    answers = []
    questions = []
    for output in decoded_outputs:
        lines = output.splitlines()
        for line in lines:
            if line.startswith("ANSWER:"):
                answers.append(line)
            elif line.startswith("QUESTION:"):
                questions.append(line)

    return questions, answers