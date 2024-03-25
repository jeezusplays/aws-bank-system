import os
from dotenv import load_dotenv
import logging
import pymysql

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", filename="./logs/setup.log")

# Load environment variables from .env file
load_dotenv()

HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")

# Decorator to catch exceptions
def trycatch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.info(f"Error: {e}")
    return wrapper

@trycatch
def setup_sql():
    logging.info("Setting up the database...")
    logging.info(f"Host: {HOST}")
    logging.info(f"User: {USER}")
    logging.info(f"Database: {DATABASE}")
    logging.info(f"Password: {PASSWORD}")
    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD)

    try:
        with connection.cursor() as cursor:
            with open("setup.sql") as file:
                sql = file.read()
                sql = sql.replace("\n", "")
                cursor.execute(sql)
                connection.commit()

    except Exception as e:
        print(f"Error: {e}")

# Call the connect function
if __name__ == "__main__":
    setup_sql()
