import openai
import os 
import json
from dotenv import load_dotenv
from db import execute
load_dotenv()
openai.api_key=os.getenv("API_KEY")
def analyze_query(userquery):
    try:
        with open('schema.txt', 'r') as file:
            schema = file.read()
            
        prompt=f"""
        Based on the following schema: {schema}
        and the following query: {userquery}
        Generate an SQL query that will either input, update, delete, or retrieve a new customer, invoice, invoice item, or item.
        If there is missing nonessentital information, please fill it in with NULL. Take into account the dependencies between the tables. Simplify the query as much as possible. Use property names enclosed in double quotes.
        Please only return the SQL in this format:
        {{
            querytype: "insert" (if delete then put delete, if update then put update, if select then put select),
            sql: "SQL query" (ONLY **VALID** SQL queries)
        }}
        """
        
        response = openai.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            model="gpt-4o",
        )
        
        text= response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        print(text)
        json_response=json.loads(text)
        print(json_response)
        response=execute(json_response)
        return response
    except Exception as e:
         print(f"Error:  An issue occurred while processing your query- {str(e)}")
         return LLM_err(e, userquery, schema, json_response)
def LLM_err(err, userquery, schema, json_response):
    prompt=f"""
    Given this error: {err}
    The query: {userquery}
    The schema: {schema}
    The JSON response: {json_response}
    Please formulate a response for the user regarding the error, but do not mention the error itself or details of the schema.
    """
    response = openai.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            model="gpt-4o",
        )
    return response.choices[0].message.content

#testing
"""
response=analyze_query("Insert a new customer with the name of John Doe, address of 1234 Elm Street, phone number of 123-456-7890, and email of johndoe@gmail.com")
print(response)
"""