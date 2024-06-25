import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'encryptiv_db',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn