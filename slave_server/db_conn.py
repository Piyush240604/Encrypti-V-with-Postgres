import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'encryptiv_db',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection() -> object:
    conn: object = psycopg2.connect(**db_params)
    return conn

if __name__ == '__main__':
    db_conn = get_db_connection()