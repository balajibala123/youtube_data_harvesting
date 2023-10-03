# Youtube Data Harvesting 

## git clone -- clone the below code to your local environmnet

git clone https://github.com/balajibala123/youtube_data_harvesting.git

## Pre-Requisite

Need to install below python install packages
 - !pip install mysql-connector-python
 - !pip install tabulate
 - !pip install pymysql
 - !pip install sqlalchemy
 - !pip install googleapiclient.discovery.build
 - !pip install google-api-python-client
 - !pip install pandas
 - !pip install pymongo
 - !pip install isodate
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

## functions in my youtube_api_version_2.py file


we've a function called overall where we're getting overall data of a channel

| Input         | Output       | functions                                       |
|---------------|--------------|-------------------------------------------------|
| channel_name  | Overall_data | Overall(channel_name)                           |

calling the below functions json data inside overall function

| Input         | Output       | functions                                       |
|---------------|--------------|-------------------------------------------------|
| channel name  | c_id         | channel(youtube, channel_name)                  |
| channel_id    | p_id         | playlistId(youtube, c_id)                       ||
| p_id          | Playlist     | videoId(youtube, p_id)                          |
| c_id          | cd (uploadid)| getChannelStats(youtube, c_id)                  |
| cd (uploadid) | Original     | getPlaylistId(youtube,cd)                       |
| Original,Playlist| final_video_id | videoIdFinal(Original,Playlist)            |
| final_video_id,cd | video_details | getVideoDetails(youtube,final_video_id,cd) ||
| final_video_id| comment_details   | getComment(youtube,final_video_id)         |
| cd (uploadid) | playlist_Names    | getPlaylistNames(youtube,cd)               |

After passing channel name data will be written into collections

| Input         | Output       | functions                                       |
|---------------|--------------|-------------------------------------------------|
| channel_name  | mongodb collection | mongoDb(channel_name)                     |              


MigrateToMySQL() we're returning all the data and inserting into mysql tables

| Input         | Output       | functions                                       |
|---------------|--------------|-------------------------------------------------|
| MongoChannelData() | channel_data (table) | ChannelDataToMySQL()               |
| MongoPlaylistData() | playlist_data (table) | PlaylistDataToMySQL()            |
| MongoVideoData() | video_data (table) | VideoDataToMySQL()                     |
| MongoCommentData() | comment_data (table) | CommentDataToMySQL()               |

we've Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10 functions which retrieves data from the mysql table for the given query

# streamlit.py

we've streamlit.py where we've our code for web interface

# .gitignore

here we're use .env file to ignore, actually we're storing all our creds and api key in .env so we don't want to upload to github for security reasons

## database_connection.py

here we've our youtube, mysql and mongodb connection parameters