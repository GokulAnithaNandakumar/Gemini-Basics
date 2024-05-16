import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from gemini_utility import (load_gemini_pro_model, load_gemini_pro_vision_model, load_embedding_model_response, gemini_pro_response)


working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="✨",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Gemini AI',
                           ['ChatBot',
                            'Image Captioning',
                            'Embed text',
                            'Ask me anything'],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  # Renamed for clarity
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


if selected=="Image Captioning":
    st.title("Narrate")

    uploadedImg=st.file_uploader("Upload a Image", type=["jpeg", "jpg", "png"])

    if st.button("Generate_Caption"):
        image=Image.open(uploadedImg)
        col1, col2=st.columns(2)

        with col1:
            resized_image=image.resize((800,500))
            st.image(resized_image)

        default_prompt="Write a short caption for this image"

        # Getting respomse
        caption=load_gemini_pro_vision_model(default_prompt, image)

        with col2:
            st.info(caption)


if selected=="Embed text":
    st.title("Embed Text")

    input_text=st.text_area(label="", placeholder="Enter the text")

    if st.button("Get Embeddings"):
        response=load_embedding_model_response(input_text)
        st.markdown(response)



if selected == "Ask me anything":

    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)