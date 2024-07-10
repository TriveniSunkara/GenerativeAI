import openai
import streamlit as st

# Sidebar to input OpenAI API key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("Chatbot")    
st.caption("A Streamlit chatbot created by me")

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
          
# Handle user input and generate a response
if prompt := st.chat_input("Type your message here..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Create an OpenAI API client and request completion
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    # Store and display assistant's response
    msg = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
