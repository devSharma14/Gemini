import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))
model = genai.GenerativeModel('gemini-pro')

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    
with open('static/index.html', 'r') as html_file:
    html_content = html_file.read()
    
with open('static/style.css', 'r') as css_file:
    css_content = f"<style>{css_file.read()}</style>"
    
st.markdown(css_content, unsafe_allow_html=True)
st.markdown(html_content, unsafe_allow_html=True)
 
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)
     
if prompt := st.chat_input("Ask me anything :) I am ready to help you out!"):
    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
 
    with st.chat_message("assistant"):
        st.markdown(response.text)
