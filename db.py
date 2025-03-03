import psycopg2
import os
from psycopg2 import sql
from dotenv import load_dotenv
load_dotenv()

def createDB():
    conn=psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute("CREATE DATABASE invoicedb")
    except psycopg2.errors.DuplicateDatabase:
        pass
    cur.close()
    conn.close()

def connectDB():
    return psycopg2.connect(
        dbname="invoicedb",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
def init_DB():
    createDB()
    conn = connectDB()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS customer (
                id SERIAL PRIMARY KEY,
                fullname TEXT UNIQUE,
                address TEXT,
                phone TEXT,
                email TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS invoice (
                id SERIAL PRIMARY KEY,
                customerid INT references customer(id),
                date DATE
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS item (
                id SERIAL PRIMARY KEY,
                item TEXT UNIQUE,
                price FLOAT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS invoiceitem (
                id SERIAL PRIMARY KEY,
                invoiceid INT references invoice(id),
                itemid INT references item(id),
                quantity INT
            );
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print("An error occurred: " + str(e))

    


def execute(sql_query):
    try:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute(sql_query['sql'])
        if "select" in sql_query['querytype']:
            response = cursor.fetchall()
        elif "insert" in sql_query['querytype']:
            response= "Inserted successfully."
        elif "delete" in sql_query['querytype']:
            response="Deleted successfully"
        elif "update" in sql_query['querytype']:
            response="Updated successfully"
        conn.commit()
        conn.close()
        print(response)
        return response
    except Exception as e:
        raise Exception(str(e))
