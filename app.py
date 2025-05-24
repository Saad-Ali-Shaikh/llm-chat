import streamlit as st
import google.generativeai as googleai
from functions import get_secret, reset_chat

api_key = get_secret("api_key")
googleai.configure(api_key=api_key)
model = googleai.GenerativeModel("gemini-2.0-flash")

# st.title("Chat with Gemini 2.0 Flash")
# st.write(
#     "This is a demo of the Gemini 2.0 Flash model. "
#     "You can ask it anything and it will try to help you."
# )
# st.markdown(
#     "This app is powered by [Streamlit](https://streamlit.io/) and [Google Generative AI](https://developers.google.com/generative-ai/)."
# )
st.subheader("Generative AI Chatbot!")
temperature = st.sidebar.slider(
    label="Select the temperature",
    min_value=0.0,
    max_value=2.0,
    value=1.0
)

if st.sidebar.button("Reset chat"):
    reset_chat()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.session_state.chat_history.append(("assistant", "Hi! How can I help you?"))

user_message = st.chat_input("Type your message here:")
for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)
if user_message:
    st.session_state.chat_history.append(("user", user_message))
    st.chat_message("user").write(user_message)
    
    # system_prompt = f"""You are a helpful assistant. 
    #                     Be kind, concise, and helpful in all your responses."""
    system_prompt = f"""
                        You are a friendly and a programming tutor.
                        Always explain concepts in a simple and clear way, using examples when possible.
                        If the user asks something unrelated to programming, politely bring the conversation back to programming topics.
                        """
    #full_input = f"{system_prompt}\n\nUser message:\n\n{user_message}\n\nChat history:\n\n"
    full_input = f"{system_prompt}\n\nUser message:\n\"\"\"{user_message}\"\"\""
    
    context = [
    *[
        {"role": role, "parts": [{"text": msg}]} for role, msg in st.session_state.chat_history
    ],
    {"role": "user", "parts": [{"text": full_input}]}]

    # response = model.generate_content(full_input)
    response = model.generate_content(context, generation_config={"temperature": temperature,"max_output_tokens": 1000})
   
    assistant_reply = response.text

    st.chat_message("assistant").write(assistant_reply)
    st.session_state.chat_history.append(("assistant", assistant_reply))
