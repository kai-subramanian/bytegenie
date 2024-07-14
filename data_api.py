import pandas as pd
import sqlite3
from pydantic import BaseModel
from google import generativeai as genai
# Load data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

events_df = pd.read_csv("data/event_info.csv")
companies_df = pd.read_csv("data/company_info.csv")
people_df = pd.read_csv("data/people_info.csv")

people_df["email"]=people_df["first_name"]+"."+people_df["last_name"]+"@"+people_df["homepage_base_url"]

print("Creating db connection")
con = sqlite3.connect("bytegenie_takehome.db",check_same_thread=False)

print("Loading tables from csv to table")
companies_df.to_sql('company', con, if_exists='append', index=False)
events_df.to_sql('events', con, if_exists='append', index=False)
people_df.to_sql('people', con, if_exists='append', index=False)

con.commit()

genai.configure(api_key="your_api_key_goes_here")
model=genai.GenerativeModel(model_name="gemini-1.5-flash")

class Query(BaseModel):
    query: str

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://192.168.1.2:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query_processor/")
async def backend_api(query: Query):
    sql_q=model.generate_content("I want you to act as an expert SQL query creator for the SQLite Database. Remember this info for all queries. Suppose you are given three data tables, named as company, events and people. The schema is as follows - Schema for company consists of the following fields - company_logo_url,company_logo_text,company_name,relation_to_event,event_url,company_revenue,n_employees,company_phone,company_founding_year,company_address,company_industry,company_overview,homepage_url,linkedin_company_url,homepage_base_url,company_logo_url_on_event_page,company_logo_match_flag. Schema for the table events consists of the following fields- event_logo_url,event_name,event_start_date,event_end_date,event_venue,event_country,event_description,event_url. Schema for the table people consists of the following fields - first_name,middle_name,last_name,job_title,person_city,person_state,person_country,email_pattern,homepage_base_url,duration_in_current_job,duration_in_current_company,email.  Events and company data can be merged using 'event_url' column. Company and people data can be merged using 'homepage_base_url' column. If the query pertains to events and people, join it using company table. Each event_url corresponds to a unique event, and each homepage_base_url can be interpreted as a unique company. Regarding preprocessing and standardising data, you have to convert the user dates from natural language to YYYY-MM-DD format. For example, if i say May 2025 you can take it as 2025-05-01. If user inputs currency value in millions or billions, convert it to numbers, for example 1 million $ = 1000000 $ and so on. If user asks for email id's, make sure that they are unique, we do not want repetitions. Use lowercase characters in where or like expressions or conditions. For event or conference names, search in both event name and description. With this info, give me proper SQL prompts with accurate schema based column names. Give me the SQLite query for - " + query.query)
    sql_query=sql_q.text
    inner_str = sql_query.split("```")[1]
    sqlite_query=str(inner_str[6:])
    print(sqlite_query)
    output = con.execute(sqlite_query)
    return output.fetchall()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)