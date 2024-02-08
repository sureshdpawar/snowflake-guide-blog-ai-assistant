import logging
import os
import sys
from typing import Any, Dict, Generator, List, Union

import openai
import streamlit as st
from llama_index import StorageContext, load_index_from_storage

# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

ResponseType = Union[Generator[Any, None, None], Any, List, Dict]

# Placeholder for the OpenAI API key
openai_api_key = ""

#@st.cache_resource(show_spinner=False)
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
    """Validate the OpenAI API key. Placeholder for actual validation logic."""
    return bool(api_key)  # Simple check to ensure the key is not empty

def main() -> None:
    """Run the chatbot."""
    global openai_api_key

    st.sidebar.title("Configuration")
    openai_api_key_input = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

    if openai_api_key_input:
        if validate_api_key(openai_api_key_input):
            openai_api_key = openai_api_key_input
            openai.api_key = openai_api_key
            st.sidebar.success("API Key accepted.")
        else:
            st.sidebar.error("Invalid API Key. Please enter a valid OpenAI API key.")
            return
    else:
        st.sidebar.warning("Please enter an OpenAI API key to enable the chat.")
        return

    if "query_engine" not in st.session_state:
        st.session_state.query_engine = load_index()

    st.title("Chat with Snowflake Blog AI Assistant!")
    # Add an image (replace 'path_to_image' with your image path or URL)
    image_path = 'blog-ai.png'  # Example: 'images/clothing.jpg' or 'http://example.com/image.jpg'
    st.image(image_path, caption='Fashion and Apparel')

    st.markdown("""
    👗 **Your Assistant**

    All about Snowpark for Data Engineering Quickstarts from quickstarts.snowflake.com. Ask away your questions!
    I built an LLM Chatbot that uses Retrieval Augmented Generation to answer questions about a particular blog or a list of blogs from snowflake technology.
        
    """)

    st.write("All about Snowpark for Data Engineering Quickstarts from quickstarts.snowflake.com. Ask away your questions!")

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

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            print("Querying query engine API...")
            # Since the actual response handling is not detailed, adjust according to your API response
            response = st.session_state.query_engine.query(prompt)
            if "Empty Response" in response.response:
                full_response = "I do not have an answer for your query. Please try other resources on our website."
            else:
                full_response = response.response

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
