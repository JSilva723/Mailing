import psycopg2

class DBConnect():
    
    def __init__(self, name, user, passwd, host):
        self.name = name 
        self.user = user 
        self.passwd = passwd 
        self.host = host 

    def get_db(self):
        # Connect with db
        db = psycopg2.connect(
            dbname=self.name, 
            user=self.user, 
            password=self.passwd, 
            host=self.host
        )
        return db

    def create_tables(self):
        # Create Table if not exist
        conn = self.get_db()
        with conn:
            with conn.cursor() as curs:
                curs.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR ( 50 ) PRIMARY KEY,
                        password VARCHAR NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS contacts (
                        email VARCHAR ( 50 ) PRIMARY KEY
                    );
                """)
