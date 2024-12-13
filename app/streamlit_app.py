import streamlit as st  
from functions import *
import base64
from pydantic import BaseModel
import time

###  DATA MODEL
class Vulnerability(BaseModel):
    cvss_score: str
    attention_note: str
    vendor: str
    affected_products: Optional[list]
    cve_identifiers: Optional[list]
    short_description: str
    score: int
    mitigation: str


def get_simple_schema(model):
    return {field: str(type_.annotation.__name__) for field, type_ in model.model_fields.items()}
def get_schema(model):
    return {field: str(type_) for field, type_ in model.model_fields.items()}
def get_theme():
    theme = st.get_option("theme.base")
    return theme

def load_streamlit_page():

    """
    Load the streamlit page with two columns. The left column contains a text input box for the user to input their OpenAI API key, and a file uploader for the user to upload a PDF document. The right column contains a header and text that greet the user and explain the purpose of the tool.

    Returns:
        col1: The left column Streamlit object.
        col2: The right column Streamlit object.
    """
    st.set_page_config(layout="wide", page_title="LLM Tool")
    # Add custom HTML for the centered image
    
    theme = get_theme()
    if theme == "dark":
        logo_path = "./image/ollama-json2.png"
    else:
        logo_path = "./image/ollama-json.png"
    st.image(logo_path, width=400)

    # Design page layout with 2 columns: File uploader on the left, and other interactions on the right.
    col1, col2 = st.columns([0.6, 0.5], gap="large")
    with col1:
        
        st.header("Tranform CISA description to structured json")
        text = st.text_area('description',height=200, key='description',
                     disabled=False)
        # Display the entered text when a button is clicked
        
    with col2:
        st.header("Model output")

    return col1, col2, text


col1, col2,text = load_streamlit_page()



if st.button("Run model"):
        start_time = time.time()
        
        with col2:
            start_time = time.time()
            structured_output = structured_outputs(Vulnerability,text)
            end_time = time.time()
            time_lapsed = end_time - start_time
            minutes, seconds = divmod(time_lapsed, 60)
            st.write(f"Execution time: {int(minutes):02d}:{int(seconds):02d}")
            st.write(structured_output)

st.header("JSON Schema")
schema = get_simple_schema(Vulnerability)
st.json(schema)
