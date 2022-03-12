import streamlit as st
import pandas as pd
import numpy as np
import transformers, torch

@st.cache  # 👈 This function will be cached
def get_model_and_tokenizer(modelpath):
  device = "cuda:0" if torch.cuda.is_available() else "cpu"
  tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2' )
  model = transformers.AutoModelForCausalLM.from_pretrained(modelpath, torch_dtype=torch.float16, low_cpu_mem_usage=True).to(device)
  return model , tokenizer

def get_message(model , tokenizer , inputSTR , top_p = 1 , temp = 0.9 , max_new_tokens=None):
  inputs = tokenizer(inputSTR, add_special_tokens=False, return_tensors="pt")["input_ids"].to(device)
  outputs = model.generate(inputs, no_repeat_ngram_size=5, max_new_tokens=max_new_tokens, top_p=top_p , temp=temp , do_sample=True , typical=0.9)
  message = tokenizer.decode(outputs[0])
  return message

st.title('Alignment TL;DR')

modelpath = "/content/drive/MyDrive/g_projects/2022/alignment-hf"
model , tokenizer = get_model_and_tokenizer(modelpath)


article_text = st.text_area('Insert excessively wordy article here: ')
tldr_button = st.button('TL;DR!')
if tldr_button:
  if len(article_text) < 1:
    st.markdown("That's too short.")
  else:
    st.markdown("Sorry, didn't read it either.")
    st.markdown(article_text)