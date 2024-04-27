import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,  BitsAndBytesConfig
from huggingface_hub import login
from constants import AUTH_TOKEN
import streamlit as st
@st.cache(allow_output_mutation=True)
def model_setup():
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    login(token=AUTH_TOKEN)

    config = BitsAndBytesConfig(
        load_in_8bit = True,
        llm_int8_threshold = 20.0,
        llm_int8_enable_fp32_cpu_offload = False,
        llm_int8_has_fp16_weight = False
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_id, trust_remote_code=True, padding=True, padding_side="left"
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=config,
        device_map="auto",
        trust_remote_code=True
    )


    return model, tokenizer