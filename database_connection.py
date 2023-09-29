import mysql.connector
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# to load the env variables
load_dotenv()

# YOUTUBE------------------------------------------------------------
#  here we're providing the youtube api key, service name and version
api_service_name = os.getenv("API_SERVICE_NAME")
api_version = os.getenv("V3")
api_key = os.getenv("API_KEY")

# MYSQL---------------------------------------------------------------
#  here we're providing mysql related database details
mysql_host_name = os.getenv("MYSQL_HOST_NAME")
mysql_user = os.getenv("MYSQL_USER_NAME")
mysql_password = os.getenv("MYSQL_USER_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE_NAME")


def MyCursor():
    db = mysql.connector.connect(
    host= f'{mysql_host_name}',
    user= f'{mysql_user}',
    password= f'{mysql_password}',
    database= f'{mysql_database}'
    )

    mycursor = db.cursor(buffered= True)
    return db,mycursor
    # db.commit()

# MONGODB--------------------------------------------------------------
# here we're providing mongodb database and collection name 

mongo_host_name = os.getenv('MONGO_HOST_NAME')
mongo_port = int(os.getenv('MONGO_PORT'))
mongo_db_name = os.getenv('MONGO_DB_NAME')
mongo_coll_name = os.getenv('MONGO_COLLECTION_NAME')

def MongoConnection():
    # creating local client connection string 
    localClient = MongoClient(f"mongodb://{mongo_host_name}:{mongo_port}")

    # creating db 
    db = localClient[mongo_db_name]

    # creating connection
    coll = db[mongo_coll_name]

    return localClient, db, coll
