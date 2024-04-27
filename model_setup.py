import torch
from transformers import pipeline, BitsAndBytesConfig
from huggingface_hub import login
from constants import AUTH_TOKEN, PROMPT_FORMAT_STRING

def model_setup():
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    login(token=AUTH_TOKEN)

    config = BitsAndBytesConfig(load_in_8bit=True)

    model_pipeline = pipeline(
        task="text-generation",
        model=model_id,
        model_kwargs={"quantization_config": config, "trust_remote_code": True, "torch_dtype": torch.qint8},
        device_map="auto"
    )

    return model_pipeline