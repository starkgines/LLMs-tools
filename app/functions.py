import pandas as pd
from typing import Optional, Sequence, List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel,Field
from ollama import Client
import json


def structured_outputs(struc_model,promp_query, model='llama3.1'):
    """
    Return a Pydantic BaseModel instance from a unstructured description input.

    Args:
        struc_model (BaseModel): The Pydantic BaseModel.
        promp_query (str): The unstructured description.
        model (str): name of the model running locally.

    """
    parser = PydanticOutputParser(pydantic_object=struc_model)
    prompt = PromptTemplate(
        template="Answer the user query, and only response a JSON format without any other text outside the format text \n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    client = Client(host='http://localhost:11434')
    response = client.chat(messages=[
    {
        'role': 'user',
        'content': prompt.format(query=promp_query),
    }
        ],
    options={'temperature': 0},
    model=model,
    format=parser.model_json_schema(),
    ) 
    structured_output = struc_model.model_validate_json(response.message.content)
    return structured_output

def save_cisa_structured_to_json(data, file_path):
    """
    Save a Pydantic BaseModel instance to a JSON file.

    Args:
        data (BaseModel): The Pydantic BaseModel instance to save.
        file_path (str): The path to the JSON file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data.dict(), file, indent=4)
        print(f"Structured data saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


