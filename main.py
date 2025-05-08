# for chroma db
#from backend.core import run_llm

# for pinecone db
from backend.core_pinecone import run_llm

import streamlit as st
from streamlit_chat import message
from PIL import Image
import os

def create_sources_string(sources: set[str]) -> str:
    if not sources:
        return ""
    sources_list = sorted(sources)
    sources_string = "Sources:\n"
    for source in sources_list:
        cleaned = source.replace("Manuals/EDW", "")
        sources_string += cleaned
    return sources_string

# Page config and header
st.set_page_config(page_title="Edelweiss Knowledge Bot", page_icon="🤖")
st.header("Edelweiss Knowledge Bot")

# Banner image
ing_image = Image.open("banner/banner_wing.jpg")
st.image(ing_image)

# Password protection with up to 3 attempts
if "password_attempts" not in st.session_state:
    st.session_state.password_attempts = 0
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("password_form", clear_on_submit=True):
        password = st.text_input("Enter password to continue:", type="password")
        submitted = st.form_submit_button("Login")
    # Stop script until form is submitted
    if not submitted:
        st.stop()
    # Require non-empty entry
    if not password:
        st.warning("Please enter the password to proceed")
        st.stop()
    # Validate password
    if password == os.getenv("BOT_PASSWORD"):
        st.session_state.logged_in = True
        # Rerun to clear the form and hide the input
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()
    else:
        st.session_state.password_attempts += 1
        remaining = 3 - st.session_state.password_attempts
        if remaining <= 0:
            st.error("Access denied. Too many failed attempts.")
            st.stop()
        else:
            st.error("Incorrect password")
            st.warning(f"You have {remaining} attempt{'s' if remaining > 1 else ''} left.")
            st.stop()

# Initialize session state for chat
if "user_promt_history" not in st.session_state:
    st.session_state.user_promt_history = []
if "chat_answer_history" not in st.session_state:
    st.session_state.chat_answer_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Track follow-up count
if "follow_up_count" not in st.session_state:
    st.session_state.follow_up_count = 0

if "draw_separator" not in st.session_state:
    st.session_state.draw_separator = False

# Input form
with st.form("promt_input", clear_on_submit=True):
    prompt = st.text_input("Prompt:", placeholder="Enter your prompt here...")
    submitted = st.form_submit_button("Submit")

    if submitted and prompt:
        # Track follow-up count
        st.session_state.follow_up_count += 1
        # Enforce history limit
        if st.session_state.follow_up_count > 5:
            st.session_state.chat_history.clear()
            st.session_state.user_promt_history.clear()
            st.session_state.chat_answer_history.clear()
            st.warning("History cleared due to reaching the limit. Starting fresh.")
            st.session_state.draw_separator = True
            st.session_state.follow_up_count = 1
        elif st.session_state.follow_up_count == 5:
            st.warning("History limit reached. It will be cleared after your next question.")
        with st.spinner("Generating response..."):
            generated_response = run_llm(prompt)

        sources = {
            f'{doc.metadata["source"][5:-4]} page {int(doc.metadata["page"])}\n'
            for doc in generated_response["source_documents"]
        }
        formatted_response = (
            f"{generated_response['answer']}"
        )
        # formatted_response = (
        #     f"{generated_response['answer']}\n\n{create_sources_string(sources)}"
        # )
        st.session_state.user_promt_history.append(prompt)
        st.session_state.chat_answer_history.append(formatted_response)
        st.session_state.chat_history.append((prompt, generated_response['answer']))

# Render chat history (newest first)
if st.session_state.chat_answer_history:
    # If a separator is pending (history was just cleared), draw it here
    if st.session_state.draw_separator:
        st.markdown("---")
        st.session_state.draw_separator = False
    # Display history with unique keys to avoid duplicate IDs
    history_items = list(zip(
        reversed(st.session_state.user_promt_history),
        reversed(st.session_state.chat_answer_history)
    ))
    for idx, (user_query, bot_response) in enumerate(history_items):
        message(user_query, is_user=True, key=f"user_{idx}")
        message(bot_response, key=f"bot_{idx}")