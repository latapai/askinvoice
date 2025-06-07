import os, pandas as pd
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import prompt_util
import prompt_humanize
import ibm_db_dbi
import ibm_db

import time
import json
import datetime

import warnings
warnings.filterwarnings("ignore")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any

app = FastAPI()


#config Watsonx.ai environment
load_dotenv()
api_key = os.getenv("API_KEY", None)
ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
project_id = os.getenv("PROJECT_ID", None)
uid = os.getenv("USER", None)
pwd = os.getenv("PASSWORD", None)
host = os.getenv("DBHOST", None)
port = os.getenv("DBPORT", None)

if api_key is None or ibm_cloud_url is None or project_id is None:
    raise Exception("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
else:
    creds = {
        "url": ibm_cloud_url,
        "apikey": api_key 
    }

def send_to_watsonxai(prompt,
                    db_object = None,
                    uc = 1,
                    #model_name="bigcode/starcoder",
                    #model_name="ibm-mistralai/mixtral-8x7b-instruct-v01-q",
                    #model_name="meta-llama/llama-2-70b-chat",
                    model_name="codellama/codellama-34b-instruct-hf",
                    decoding_method="greedy",
                    max_new_tokens=100,
                    min_new_tokens=30,
                    temperature=1.0,
                    repetition_penalty=1.0
                    ):
    
    #assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "make sure none of the prompts in the inputs prompts are empty"

    if(model_name == "bigcode/starcoder" or model_name == "codellama/codellama-34b-instruct-hf"):
        model_params = {
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MIN_NEW_TOKENS: 1,
                GenParams.MAX_NEW_TOKENS: 400,
                # GenParams.DECODING_METHOD: "Sampling",
                # GenParams.MAX_NEW_TOKENS: 300,
                # GenParams.TEMPERATURE: 0.7,
                GenParams.STOP_SEQUENCES:[";"],
                # GenParams.REPETITION_PENALTY: 1
                # GenParams.TOP_K: 50,
                # GenParams.TOP_P: 1,
                # GenParams.RANDOM_SEED: 63,
            }
    else:
        model_params = {
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MIN_NEW_TOKENS: 1,
                GenParams.MAX_NEW_TOKENS: 2000,
                GenParams.STOP_SEQUENCES:["\n\n"],
            }
    
    # Instantiate a model proxy object to send your requests
    model = Model(
        model_id=model_name,
        params=model_params,
        credentials=creds,
        project_id=project_id)
    
    if(model_name == "bigcode/starcoder" or model_name == "codellama/codellama-34b-instruct-hf"):
        print("Code LLM Called ===>")
        llm_response = model.generate_text(prompt)
            
    else:
        print("Text LLM Called ===>")
        llm_response = model.generate_text(prompt)
    return llm_response

def db_connection():
    db2_dsn = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL'.format(
        'bludb',
        host,
        port,
        uid=uid,
        pwd=pwd
    )
    return ibm_db.connect(db2_dsn,"","")

command_ = prompt_util.command
references_ = prompt_util.references
schema_ = prompt_util.schema
notes_ = prompt_util.notes
examples_ = prompt_util.examples
pattern = """{command}
	Schema: {schema} 
    {examples}
	Input: {request}
	Output: """
prompt_template = PromptTemplate.from_template(pattern)

instruction_human_ = prompt_humanize.instruction_human
examples_human_ = prompt_humanize.examples_human
pattern_human = """{instruction_human}
    {examples_human}
	Input: {request}
    Table: {table}
	Output: """
prompt_template_human = PromptTemplate.from_template(pattern_human)

class InputText(BaseModel):
    query: str

class ProcessedText(BaseModel):
    error: bool
    message: str
    table: Any
    sql: str

@app.post("/process/", response_model=ProcessedText)
def process(input_text: InputText):
        data = input_text.query
        if data:
            prompt = prompt_template.format(command = command_, 
									schema = schema_,
									references = references_,
									examples = examples_,
									notes = notes_,
									request = data)
            start_time_query = time.time()
            connection = db_connection()
            conn = ibm_db_dbi.Connection(connection)
            response = send_to_watsonxai(prompt=prompt)
            if("LLM chain error:" in response):
                return {
                    "error" : True,
                    "message": response,
                    "table": None,
                    "sql": None
                }
            print("Query generated ===>\n",response)
            stop_time_query = time.time()
            start_time_db = time.time()
            sql_query = response
            try:
                print("Creating dataframe from SQL query ===>")
                df = pd.read_sql(sql_query, conn)
            except Exception as err:
                print("Error while trying to create dataframe===>\n",err)
                print("Duration 1st Call: ",stop_time_query - start_time_query)
                return {
                    "error" : True,
                    "message": str(err),
                    "table": None,
                    "sql": None
                    }
            print(df)
            stop_time_db = time.time()
            df = df.loc[:,~df.columns.duplicated()].copy()
            rows = len(df.axes[0])
            if(rows > 0):
                for col in df.columns:
                    dtype = type(df[col].iloc[0])
                    if(dtype is datetime.date):
                        print("converting type to string for column: ",col)
                        df[col] = df[col].astype(str)
            table_html = df.to_html()
            if(rows>4):
                print("Big table encountered! Returning 10 rows from table.")
                print("Duration 1st Call: ",stop_time_query - start_time_query)
                print("Duration DB Call: ",stop_time_db - start_time_db)
                return {
                "error" : False, 
                "message": "",
                "table": json.loads(df.to_json(orient='records', force_ascii=False))[0:10],
                "sql": sql_query
                }
            start_time_human = time.time()
            prompt_human = prompt_template_human.format(instruction_human = instruction_human_, 
                                examples_human = examples_human_,
                                request = data,
                                table = table_html)
            response_humanized = send_to_watsonxai(prompt=prompt_human, model_name='mistralai/mixtral-8x7b-instruct-v01')
            stop_time_human = time.time()
            print("Duration 1st Call: ",stop_time_query - start_time_query)
            print("Duration DB Call: ",stop_time_db - start_time_db)
            print("Duration 2nd Call: ",stop_time_human - start_time_human)
            print("Total Time: ",stop_time_human-start_time_query)
            print("Humanized response generated ===>\n",response_humanized)
            return {
                "error" : False, 
                "message": response_humanized,
                "table": json.loads(df.to_json(orient='records', force_ascii=False))[0:10],
                "sql": sql_query
                }
        print("No Error, but something went wrong!")
        return {
            "error" : True,
            "message": "No Error, but something went wrong!",
            "table": None,
            "sql": None
            }