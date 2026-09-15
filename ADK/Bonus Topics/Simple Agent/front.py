import uuid
import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="ADK Chat", page_icon="🤖")
st.title("ADK Agent Chat")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={
            "message": prompt,
            "user_id": st.session_state.user_id,
            "session_id": st.session_state.session_id,
        },
    )
    data = response.json()
    st.session_state.session_id = data["session_id"]

    with st.chat_message("assistant"):
        st.markdown(data["reply"])
    st.session_state.messages.append({"role": "assistant", "content": data["reply"]})