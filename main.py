from backend.core import run_llm

import streamlit as st
from streamlit_chat import message

from PIL import Image


def create_sources_string(sources: set[str]) -> str:
    if not sources:
        return ""
    sources_list = list(sources)
    sources_list.sort()
    sources_string = "Sources:\n"
    for source in sources_list:
        source = source.replace("Manuals/EDW", "")
        sources_string += source
    return sources_string


st.set_page_config(page_title="Edelweiss Knowledge Bot", page_icon="🤖")

st.header("Edelweiss Knowledge Bot")
image = Image.open("banner/banner_wing.jpg")
st.image(image)

if "user_promt_history" not in st.session_state:
    st.session_state["user_promt_history"] = []
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

with st.form("promt_input", clear_on_submit=True):
    prompt = st.text_input("Prompt:", placeholder="Enter your promt here...")
    submitted = st.form_submit_button("Follow up")
    submitted_new = st.form_submit_button("New topic")

    if submitted and prompt:
        with st.spinner("generating response..."):
            generated_response = run_llm(
                query=prompt, chat_history=st.session_state["chat_history"]
            )

            sources = set(
                [
                    f'{doc.metadata["source"][5:-4]} page {int(doc.metadata["page"])}\n'
                    for doc in generated_response["source_documents"]
                ]
            )
            formatted_response = (
                f"{generated_response['answer']} \n\n{create_sources_string(sources)}"
            )
            st.session_state["user_promt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)
            st.session_state["chat_history"].append(
                (prompt, generated_response["answer"])
            )
    if submitted_new and prompt:
        st.session_state["chat_history"] = []
        st.session_state["user_promt_history"] = []
        st.session_state["chat_answer_history"] = []

        with st.spinner("Generating response.."):
            generated_response = run_llm(query=prompt)
            sources = set(
                [
                    f'{doc.metadata["source"][5:-4]} page {int(doc.metadata["page"])}\n'
                    for doc in generated_response["source_documents"]
                ]
            )

            formatted_response = (
                f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
            )

            st.session_state["user_promt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)
            st.session_state["chat_history"].append(
                (prompt, generated_response["answer"])
            )


if st.session_state["chat_answer_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answer_history"], st.session_state["user_promt_history"]
    ):
        message(user_query, is_user=True)
        message(generated_response)
