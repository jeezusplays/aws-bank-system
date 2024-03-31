from rds import *
from dynamo import *

if __name__ == "__main__":
    setup_sql()
    reset_database()
    insert_mock_data()