# Youtub Data Harvesting 

## Pre-Requisite

Need to install below python install packages
 - pip install mysql-connector-python
 - pip install tabulate
 - pip install pymysql
 - pip install sqlalchemy
 - pip install googleapiclient.discovery.build
 - pip install google-api-python-client
 - pip install pandas
 - pip install pymongo
 - pip install isodate
 - !pip install streamlit
 - !pip install python-dotenv

 ## To setup we need to have few keys and password in .env file

 ## youtube api keys
 - **API_KEY = 'your api keys'**
 - **V3 = 'your version number'**
 - **API_SERVICE_NAME = "your service name"**

## MYSQL DB DETAILS 
 - **MYSQL_HOST_NAME = replace host name**
 - **MYSQL_USER_NAME = replace mysql user name**
 - **MYSQL_USER_PASSWORD = replace mysql password here**
 - **MYSQL_DATABASE_NAME = replace your database name here**

## Mongo DB details
 - **MONGO_HOST_NAME = replace host name**
 - **MONGO_PORT = replace port number**
 - **MONGO_DB_NAME = replace db name**
 - **MONGO_COLLECTION_NAME = replace collection name**

## To run the code please enter the below command in terminal
 
streamlit run streamlit.py

once executed the above code you'll get a localhost:port to navigate the web app link