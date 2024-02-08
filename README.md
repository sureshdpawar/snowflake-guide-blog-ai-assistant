# Building a Snowflake Blog AI assistant using Retrieval Augmented Generation

## Overview

In this guide, we will build an LLM Chatbot that uses Retrieval Augmented Generation to answer questions about a particular blog or a list of blogs. We use LlamaIndex to chunck the blog text and build index, and then provide this context from the blog chunks along with the prompt to the GPT-4 model to build the chatbot.

By the end of this session, you will have an interactive web application deployed that helps answer questions from the blog.

## Step-By-Step Guide

For prerequisites, environment setup, step-by-step guide and instructions, 

set the virtual env
```
python -m venv env
```

for windows activate environment

```
 .\env\Scripts\activate 
```
for linux activate environment
```
source /env/bin/activate
```

install the dependancies

```
pip install -r requirements.txt
```

optional as i have already performed these steps

```
python data_pipeline.py
python build_index.py
```
run the app

```
streamlit run streamlit_app.py
```

references:
please refer to the https://quickstarts.snowflake.com/guide [](https://quickstarts.snowflake.com/guide/build_rag_based_blog_ai_assistant_using_streamlit_openai_and_llamaindex/index.html?index=..%2F..index#0).

