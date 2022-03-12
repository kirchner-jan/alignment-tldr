import streamlit as st
import pandas as pd
import numpy as np
import requests , html

def get_payload(article_text):
  payload = {"context":html.escape(article_text), "top_p": 0.9, "temp": 0.75}
  return payload
def main():
  st.title('Alignment TL;DR')
  model_url = st.text_area('Insert address that accepts requests: ')
  article_text = st.text_area('Insert excessively wordy article here: ')
  context = '\n\nTL;DR:'
  tldr_button = st.button('TL;DR!')
  if tldr_button:
    if len(article_text) < 1:
      st.markdown("That's too short.")
    else: 
      if len(article_text) > 1000:
        st.markdown("That's too long, I'll skip some of that.")
      article_text = article_text[:5000]
      payload = get_payload(article_text + context)
      r = requests.post(model_url, json=payload)
      completion = r.json()["completion"][len(article_text)+5:]
      completion = completion.split('<|endoftext|>')[0]
      st.markdown(completion)

if __name__ == '__main__':
    main()
