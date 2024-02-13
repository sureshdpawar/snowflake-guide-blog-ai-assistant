import logging
import os
import sys
from typing import Any, Dict, Generator, List, Union
import requests
import streamlit as st
import openai  # Ensure this is added to use OpenAI's API
from llama_index import StorageContext, load_index_from_storage

# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

ResponseType = Union[Generator[Any, None, None], Any, List, Dict]

def load_index() -> Any:
    """Load the index from the storage directory."""
    print("Loading index...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".kb")
    storage_context = StorageContext.from_defaults(persist_dir=dir_path)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    print("Done.")
    return query_engine

def validate_api_key(api_key: str) -> bool:
    """Validate the OpenAI API key by attempting a test API call."""
    url = "https://api.openai.com/v1/models"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code == 200:
        print("Valid key")
        return True
    else:
        print("Invalid key")
        return False

def main() -> None:
    st.sidebar.title("Configuration")
    openai_api_key_input = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

    st.title("Chat with Snowflake Blog AI Assistant!")
    image_path = 'blog-ai.png'  # Ensure this path is correct or adjust as needed
    st.image(image_path, caption='Snowflake Blog AI Assistant')

    st.markdown("""
    👗 **Your Assistant**
    All about Snowpark for Data Engineering Quickstarts from quickstarts.snowflake.com. Ask away your questions!
    I built an LLM Chatbot that uses Retrieval Augmented Generation to answer questions about a particular blog or a list of blogs from snowflake technology.

    **How It Works:**
    Just type your query, like below \n
    how to load table into dataframe? \n
    how to add security to dataframe?
    """)

    # Enable chat box only if API key is valid
    if openai_api_key_input and validate_api_key(openai_api_key_input):
        openai.api_key = openai_api_key_input
        st.sidebar.success("API Key accepted.")

        if "query_engine" not in st.session_state:
            st.session_state.query_engine = load_index()

        if "messages" not in st.session_state:
            system_prompt = (
                "Your purpose is to answer questions about specific documents only. "
                "Please answer the user's questions based on what you know about the document. "
                "If the question is outside the scope of the document, please politely decline. "
                "If you don't know the answer, say `I don't know`."
            )
            st.session_state.messages = [{"role": "system", "content": system_prompt}]

        for message in st.session_state.messages:
            if message["role"] not in ["user", "assistant"]:
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask your question:"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with (st.chat_message("assistant")):
                message_placeholder = st.empty()
                print("Querying query engine API...")
                response = st.session_state.query_engine.query(prompt)
                full_response = response
                if "Empty Response" in response.response:
                    full_response = "I do not have an answer for your query. Please try other resources on our website."
                else:
                    full_response = response.response
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        if openai_api_key_input:  # This condition will be true if an API key was entered but is invalid.
            st.sidebar.error("Invalid API Key. Please enter a valid OpenAI API key.")
        else:
            st.sidebar.warning("Please enter an OpenAI API key to enable the chat.")

if __name__ == "__main__":
    main()
