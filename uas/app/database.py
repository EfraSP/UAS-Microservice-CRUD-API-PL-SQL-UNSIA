import psycopg2

conn = psycopg2.connect(
    dbname="microservice",
    user="postgres",
    password="123123123",
    host="localhost",
    port="5432"
)

conn.autocommit = True
