import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="Conversational Q&A Chatbot", page_icon="💬")
st.title("🤖 Conversational Q&A Chatbot")

# Initialize session state
if "flowmessages" not in st.session_state:
    st.session_state["flowmessages"] = [SystemMessage(content="You are a helpful AI assistant.")]
if "user_started" not in st.session_state:
    st.session_state["user_started"] = False

# Display chat history
for msg in st.session_state["flowmessages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.content)

# Chat input
user_input = st.chat_input("Ask me anything")

if user_input:
    st.session_state["user_started"] = True
    st.session_state["flowmessages"].append(HumanMessage(content=user_input))
    response = ChatGroq(temperature=0.6, model_name="llama3-70b-8192")(st.session_state["flowmessages"])
    st.session_state["flowmessages"].append(AIMessage(content=response.content))

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.content)
