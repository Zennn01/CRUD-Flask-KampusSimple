import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="flaskdb",
        user="postgres",
        password="admin123",
        cursor_factory=RealDictCursor
    )