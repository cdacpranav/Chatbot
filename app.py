import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
import os

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"

# Streamlit page setup
st.set_page_config(page_title="Conversational Q&A Chatbot", page_icon=":robot_face:", layout="centered")
st.title("🤖 Conversational Q&A Chatbot")

# Initialize the model
chat = ChatGroq(
    temperature=0.6,
    model_name="llama3-70b-8192"
)

# Initialize session state for messages
if "flowmessages" not in st.session_state:
    st.session_state["flowmessages"] = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]

# Display chat history using st.chat_message (optional: cleaner UX)
for msg in st.session_state["flowmessages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.content)

# Input box at bottom 
user_input = st.chat_input("Ask me anything")

if user_input:
    # Append user's message
    st.session_state["flowmessages"].append(HumanMessage(content=user_input))

    # Generate and append AI response
    response = chat(st.session_state["flowmessages"])
    st.session_state["flowmessages"].append(AIMessage(content=response.content))

    # Show user and assistant messages right away
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.content)
