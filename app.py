# Author: Swami Chandrasekaran
# Last Updated: 06/23/2023
#
# This code is meant to serve as a template / boilerplate for building LLM based apps.
# Feel free to expand, extent and enhance.

import os
import random
from datetime import datetime
import vertexai
import streamlit as st
from langchain import OpenAI, PromptTemplate
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

# Global Settings and Config
project_id = "learning-351419"
loc = "us-central1"
primary_model_name = "text-bison@001"
temperature = 0.2
max_output_tokens = 1024
top_p = 0.8
top_k = 40
location = "us-central1"
model_name = "text-bison@001"
vertexai.init(project=project_id, location=loc)


@st.cache_resource
def generate_random_input():
    INPUT_TEXT_TMP = ""
    sample_code_gen_qns = ["Generate a semantic HTML and Tailwind CSS Contact Support form consisting of the user name, email, issue type, and message. The form elements should be stacked vertically and placed inside a card", "Write a JavaScript function. It accepts a full name as input and returns avatar letters.", "Write an Express.js API to fetch the current user's profile information. It should make use of MongoDB", "The database has students and course tables. Write a PostgreSQL query to fetch a list of students who are enrolled in at least 3 courses.", "Write a function that checks if a year is a leap year.",]
    
    INPUT_TEXT_TMP = random.choice(sample_code_gen_qns)
   
    if 'INPUT_TEXT_TMP' not in st.session_state:
        st.session_state.INPUT_TEXT_TMP = INPUT_TEXT_TMP
    elif 'INPUT_TEXT_TMP' in st.session_state:
        st.session_state.INPUT_TEXT_TMP = INPUT_TEXT_TMP
    return INPUT_TEXT_TMP

@st.cache_resource
def generate_code(txt):
    PROJECT_ID = "learning-351419"  # @param {type:"string"}
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Prompt Template
    prompt_template = """You are a master software engineer. Based on the requirements provided below, write the code following solid Python programming practices. Add relevant code comments. Don't explain the code, just generate the code.
    {text}
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    res = None

    # Instantiate the LLM model
    try:
        llm = VertexAI(model_name=primary_model_name, max_output_tokens=506,
                       temperature=0.1, top_p=0.8, top_k=40, verbose=True,)

        # Text summarization
        try:
            chain = LLMChain(prompt=PROMPT, llm=llm)
            res = chain.run(txt)
        except Exception as e:
            st.error("Error during LLM model chaining and invocation")
            st.error(e)
    except Exception as e:
        st.error("Error during LLM model initialization")
        st.error(e)

    return res

# Page title
st.set_page_config(page_title="Generative AI Text Summarization App",
                   page_icon=":random:", layout="centered")
st.title('📚 Generative AI Text Summarization App')

# Create a file upload widget for the credentials JSON file
creds_file = st.file_uploader(
    "Upload Google Cloud credentials file", type="json")

result = []
if creds_file is not None:
    now = datetime.now()
    randomfilename = "temp_credentials_" + now.strftime("%m%d%Y_%H%M%S")

    creds_contents = creds_file.read().decode("utf-8")
    with open(randomfilename, "w") as f:
        f.write(creds_contents)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = randomfilename
    
    # Using the "with" syntax
    #with st.form(key='sdlc_form', clear_on_submit = False):
    text_input = st.text_area('Tell me about your app', generate_random_input(), height=200, key='fav1')
    submit_button = st.button('Submit', key='rand1')
    
    col1, buff, col2 = st.columns([2,1,2])
    
    if submit_button:
        with st.spinner('Wait for the magic ...'):
            with col1:
                response = generate_code(text_input.strip())
                result.append(response)

                # Display result
                if len(result):
                    st.write(response)
                
            with col2:
                st.write("place holder for test cases")
