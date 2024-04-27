from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class question_dataset(Dataset):
    def __init__(self, data_path: str, tokenizer, max_length=1024):
        self.data = pd.read_csv(data_path)
        self.tokenizer = tokenizer
        self.max_length = max_length
        #generate a dictionary of the question Ids with their text
        self.question_dict = {}
        self.context_dict = {}
        self.student_answer_dict = {}
        self.label_encoder = LabelEncoder()

    def _tokenize(self):
        pass

    def __getitem__(self, idx):
        pass


def generate_prompts(questions, contexts, student_answers, tokenizer, max_length=1024):
    """
    Generate batched prompts for the model to evaluate the answer
    """
    prompts = []
    for question, context, student_answer in zip(questions, contexts, student_answers):
        prompt = f"question: {question} context: {context} student answer: {student_answer}"
        prompts.append(prompt)
    # Use a batched tokenizer for optimization
    batched_prompts = tokenizer(prompts, max_length=max_length, padding="max_length", truncation=True, return_tensors="pt")
    return batched_prompts