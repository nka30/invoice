# Invoice Web Application

Web application using Flask and PostgreSQL to store customer, item and invoice information. 

### Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running

Set up environment variables in a `.env` file:
    ```env
    SECRET_KEY=your_secret_key
    DB_USER=your_db_user
    DB_PASS=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    API_KEY=your_genai_api_key
    ```

Run the application:
    ```
    flask run
    ```
    
Open a browser and go to `http://127.0.0.1:5000/` to use the application.

IMPROVEMENT NEEDED: 
- Need to improve prompt engineering to reduce SQL errors
- More testing needed
