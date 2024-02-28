import streamlit as st
from langchain.llms import Ollama


import base64

# Define color styles for user and assistant messages
user_color = "#333"
assistant_color = "#007bff"


hide_close_icon_css = """
<style>
.st-emotion-cache-ch5dnh {
        display: none;
    }
</style>
"""
st.sidebar.markdown(hide_close_icon_css, unsafe_allow_html=True)


 # Function to convert image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load and display sidebar image with glowing effect
img_path = "imgs/scb-logo.png"
img_base64 = img_to_base64(img_path)
st.sidebar.markdown(
    f'<img src="data:image/png;base64,{img_base64}" height="60">',
    unsafe_allow_html=True,
)
st.sidebar.title("MSBR")

st.sidebar.markdown("---")




# Example usage
custom_chat_message("Hello there!", "user")
custom_chat_message("Welcome to my app!", "assistant")



# Initialize Ollama
ollama = Ollama(model="api-secexpert")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for string dialogue
def get_string_dialogue(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    return f"{string_dialogue} {prompt_input} Assistant: "

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = st.write_stream(ollama.stream(get_string_dialogue(prompt)))
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
