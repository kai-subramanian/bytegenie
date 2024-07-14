### bytegenie
This repo contains the DB and API for takehome assessment. Frontend can be found here - https://github.com/kai-subramanian/natural-query
Tech stack used - Python for backend API, React for frontend, SQLite for the database.

<p>
   <h3><b>The Backend API</b></h3>
<ol>
  <li>The main steps and motivation for any data engineering/processing on the raw data
before making it available to the API
  <p>
    The backend does the processing part of converting the raw csv data to a table within the database. We also do a modification of creating email ID and storing it in separate column in the people table. Next, we are using pandas to convert the csv data to SQLite tables. As per the test document summary, we are using three tables - company, events and people. <br><br> <b>The overall code flow of the backend is as follows -</b><br><br> We first import the required libraries and load the csv files into pandas dataframe. These dataframes are then modified to create email id, and stored in separate column. Next, we need to store them as tables in the DB. For that, we use the SQLite3 module from python, and use pandas to_sql method that writes the three dataframes - companies_df, events_df, people_df to the respective databases -  company, events and people. We are commit and keeping the connection object open as we need it to run queries later. Next, we create a connection to the genai model. For this demo, we are using Google Gemini API, using the gemini-1.5-flash model. We do some processing to allow CORS (Cross origin resource sharing), a feature used to allow client apps to use resources from a different domain. <br><br> </p></li>
  <li> The main functionalities of the API <br><br>
  <p>Next, we are going to define the API. It takes the query as a parameter and uses it to feed into Google Gemini's chat API. To get accurate results, we do some prompt engineering and fine tuning using the database schemas so it gives accurate SQL query results. We also provide user instructions, such as returning unique emails, converting word numbers to numerals (for ex, 1 million = 1000000 ) and last but not the least, we ask to standardise the dates (for ex, May 2024 = 2024-05-01). The natural language query is then converted to an SQL query by Google Gemini and returns the text block. This intermediate output is then further preprocessed in order to extract only the SQL query from Gemini's response. This SQL query is then executed against the database using the connection, and the output is returned by the API.
  </p>
  </li>
  <li> The challenges faced - <br><br>
  <ul> 
    <li>I chose to go with SQLite DB, as it had great support with Python, and was lightweight. But, while exposing the API endpoint and testing, I found that SQLite would only allow requests from the same thread ID. As a result, I had to dig deep and found that there was an option to disable checking whether the request came from the same thread or not. Another option is to create the cursor within the same method where we are using it.</li>
    <li>The async API did not allow query to be executed as a string and it threw an error 422, unprocessable entity. It wanted the text alone and not the JSON payload. Hence, i did some server side processing and imported the Pydantic library, and used the BaseModel to extract the query string alone from the request body. </li>
  </ul>
  </li>
-
<li>How would you improve the backend, if you had more time to work on it?</li>
  <ul> 
    <li>The schema for the database is unclean and I did not follow any data manipulation / extrapolation methods and just used what was supplied. I would attempt to clean the raw data more.</li>
    <li>The API works fine, but it feels hacked together. I did not follow any engineering best practices, such as writing SOLID code or any data / error checking which is output at various stages (from the Gemini LLM, from the query, from the DB, etc). I would address this on priority based on further requirements.  </li>
        <li>We do have a major risk while depending on LLMs to convert natural language to SQL queries, such as data leak, and risk of malicious SQL queries as well. Since I do not have very powerful hardware, sufficient enough to train LLMs I was not able to train a LLM model on my local laptop and had to rely on a hosted LLM such as Google Gemini. Once we get powerful hardware resources we can train a local LLM model and optimize it exclusively for SQL queries.</li>
    <li>The security is lagging in my code, I would attempt to integrate authentication into the API.</li>
     <li>Various other performance upgrades, such as fine tuning the LLM.</li>
  </ul>
</ol>

<h3><b>The DB</b></h3>
<ol>
<li>The database schema<br><br>
  The db schema for each table is given below-
  <ol>
    <li>
      Company - <br> company_logo_url,company_logo_text,company_name,relation_to_event,event_url,company_revenue,n_employees,company_phone,company_founding_year,company_address,company_industry,company_overview,homepage_url,linkedin_company_url,homepage_base_url,company_logo_url_on_event_page,company_logo_match_flag
    </li>
    <li>
      Events - <br> event_logo_url,event_name,event_start_date,event_end_date,event_venue,event_country,event_description,event_url
    </li>
    <li>
      People - <br> first_name,middle_name,last_name,job_title,person_city,person_state,person_country,email_pattern,homepage_base_url,duration_in_current_job,duration_in_current_company,email
    </li>
  </ol>
</li>
<li>The challenges you faced in working with this data<br><br>
  <ul>
    <li>The csv data had many missing entries such as duration_in_current_job and duration_in_current_company, which might lead to inconsistencies while processing with the data. </li>
    <li>Data cleansing / extrapolation was hard, given that it was qualitative data.</li>
   </ul>
</li>
<li>How would you improve the database design if you had more time to work on
it?<br><br>
  <ul>
    <li>
      I did not follow the email pattern given in the table. Since there was missing data, I decided to go with a standard approach of using firstname.lastname@organization_name and if i had more time, I would write a separate function to handle inconsistency and parse the names and use the email pattern provided.</li>
        <li>
      Since this was a test / PoC type of project, I did not spend much time in best practices such as establishing a proper data pipeline, or checking for scalability. I would add these, if the opportunity comes. </li>
  </ul>
</li>
Steps to run the program - <br>
1. Clone the frontend code from https://github.com/kai-subramanian/natural-query <br>
2. Clone the backend API repo from https://github.com/kai-subramanian/bytegenie <br>
3. Kindly delete the provided takehome_bytegenie.db as the data_api will recreate the db. Not deleting the existing db will cause some errors. <br>
   a. Kindly replace the api key in data_api.py with an API from Google Gemini. You can get one here for free - https://aistudio.google.com/app/apikey <br>
4. Run the backend code from one terminal, using python data_api.py <br>
5. From another terminal, go into the natural-query folder (frontend) <br>
6. Once inside, install the dependencies for the frontend, by running npm install <br>
7. Then, run npm start. <br>
8. You should see the app open in localhost:3000 <br>
9. The logs can be viewed in the terminal that runs the server.<br>
Thank you for considering my assessment! 
</ol></p>
