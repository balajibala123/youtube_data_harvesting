# pip install mysql-connector-python
# pip install tabulate
# pip install pymysql
# pip install sqlalchemy
# pip install googleapiclient.discovery.build
# pip install google-api-python-client
# pip install pandas
# pip install pymongo
# pip install isodate

from googleapiclient.discovery import build
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from datetime import timezone
from isodate import parse_duration
import json
from database_connection import MyCursor
from database_connection import api_service_name,api_version, api_key
from database_connection import MongoConnection


youtube = build(
    api_service_name, api_version, developerKey=api_key)

youtube

# --------------------------
# -- get channel Name-------
# --------------------------

def channel(youtube, channel_name):
    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q= channel_name
    )
    response = request.execute()


    # name= response['items'][0]['id']['channelId']
    name= response['items'][0]['snippet']['channelId']

    return name

# getting playlist id using playlists
# input - channel id here

def playlistId(youtube, c_id):
    # c_id=channel(youtube, channel_name)
    lis=[]

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=c_id,
        maxResults=25
    )
    response = request.execute()

    
    for i in range(len(response['items'])):
        data =response['items'][i]['id']

        lis.append(data)

    return lis

# getting playlist id,video id and title using playlistid(youtube) function
# input -- playlistId(youtube) here

def videoId(youtube, p_id):

    # lst= playlistId(youtube,channel_name)

    lis1=[]

    for j in p_id:
        
        request = youtube.playlistItems().list(
                    part="contentDetails,id,snippet,status",
                    playlistId= j,
                    
                    maxResults=50,
                    
        )
        response = request.execute()

        
        for i in range(len(response['items'])):

            data = response['items'][i]['contentDetails']['videoId']
            # data = dict(title =response['items'][i]['snippet']['title'],
            #             videoid=response['items'][i]['contentDetails']['videoId'],
            #             playlistid=j)

            lis1.append(data)

            

    return lis1


# ------------------------------------------------
# -----Original getChannelStats-------------------
# ------------------------------------------------

def getChannelStats(youtube, c_id): 

    # c_id = channel(youtube, channel_name)
    # all_data =[]
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics,id",
    id=c_id)

    response = request.execute()

    # for i in range(len(response['items'])):
    data = dict(Channel_Name = response['items'][0]['snippet']['title'],
                Channel_Id = response['items'][0]['id'],           
                Subscription_Count = response['items'][0]['statistics']['subscriberCount'],
                Channel_views = response['items'][0]['statistics']['viewCount'],
                Channel_Description= response['items'][0]['snippet']['description'],
                Playlist_Id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                video_Count= response['items'][0]['statistics']['videoCount'])
    
    # all_data.append(data)

    # data_1 = {response['items'][0]['snippet']['title'] : data}
    # data_1 = dict(Channel_Name_Header = response['items'][0]['snippet']['title'],
    #               Channel_detail = data)

    # return data_1
    return data


# -------------------------------------
# ----Original getting playlistid------
# -------------------------------------
# after passing playlistid we're getting video ids

def getPlaylistId(youtube,df1):
    video_id=[]
    token =None
    while True:
        # df = getChannelStats(youtube, channel_name)
        # playlist_id= df['Playlist_Id']
        request = youtube.playlistItems().list(
                    part="contentDetails,id,snippet,status",
                    playlistId= df1,
                    
                    maxResults=50,
                    pageToken = token
        )
        response = request.execute()

        # video_id=[]

        for i in range(len(response['items'])):
            video_id.append(response['items'][i]['contentDetails']['videoId'])

        
        token = response.get('nextPageToken')

        if token is None:
            break
    return video_id

def videoIdFinal(Original,Playlist):
    # 705> 372 true
    tp=[]
    # Original = getPlaylistId(youtube, channel_name)
    # Playlist = videoId(youtube,channel_name)
    
    if (len(Original))> (len(Playlist)):
        # tp=[]
        for i in Original:
            if i not in tp:
                tp.append(i)
        for i in Playlist:
            if i not in tp:
                tp.append(i)

        
    elif (len(Original)) == (len(Playlist)):
        # tp=[]
        for i in Original:
            tp.append(i)
        
    # 200<372  false
    elif (len(Original)) < (len(Playlist)):
        # tp=[]
        for i in Playlist:
            tp.append(i)
        
    return tp

# ----------------------------------------
# -----original getting video details-----
# ----------------------------------------

def getVideoDetails(youtube,video_ids,df1):
    
    # video_id = videoIdFinal(Original,Playlist)

    # df = getChannelStats(youtube, c_id)
    # df1 = df['Playlist_Id']

    # df['Playlist_Id']

    all_vid_stats =[]

    
    for i in range(0, len(video_ids),50):  #total len of video id is around 3800 something  (0, 3800, 50)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
        
            id=','.join(video_ids[i:i+50]),
            
            )
        response = request.execute()    #this will hold 50 details for the first time 



        # comments = []
        for video in response['items']:   #i'm returning 50 videos details with the help of loop
            video_stats = dict(Video_Id= video['id'],
                            Playlist_Id = df1,
                            Video_Name = video['snippet']['title'],
                            Video_Description = video['snippet']['description'],
                            #    Tags = video['snippet'].get('tags'),
                            PublishedAt = video['snippet']['publishedAt'],
                            View_Count = video['statistics']['viewCount'],
                            Like_Count = video['statistics'].get('likeCount'),
                            Favorite_Count = video['statistics']['favoriteCount'],
                            Comment_Count = video['statistics'].get('commentCount'),
                            Duration = video['contentDetails']['duration'],
                            Thumbnail = video['snippet']['thumbnails']['default']['url'],
                            Caption_Status = video['contentDetails']['caption'],
                            #    Comments = getcomment

                            )

            all_vid_stats.append(video_stats)
            
            

    return all_vid_stats
      



# -------------------------------------------
# ---- original getting comments-------------
# -------------------------------------------

def getComment(youtube,video_ids):

    # video_id = videoIdFinal(youtube,channel_name)
    
    comments=[]
    # token = None
    
    for i in video_ids:

        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=i,
            maxResults= 2
            # pageToken = token
        )
        
        try:
            # while True:
                response = request.execute()

        # comments=[]
            
                for j in range(0,len(response['items'])):
                    comment = dict(Comment_Id = response['items'][j]['snippet']['topLevelComment'].get('id',"no id"),
                                Video_Id = i,
                            Comment_Text = response['items'][j]['snippet']['topLevelComment']['snippet'].get('textDisplay', "No comments"),
                            Comment_Author= response['items'][j]['snippet']['topLevelComment']['snippet'].get('authorDisplayName',"no author"),
                            Comment_PublishedAt= response['items'][j]['snippet']['topLevelComment']['snippet'].get('publishedAt',"no time"),
                            Like_Count= response['items'][j]['snippet']['topLevelComment']['snippet'].get('likeCount',"no likes"),
                            Reply_Count= response['items'][j]['snippet'].get('totalReplyCount',"no count")
                            )
                    comments.append(comment)


                # token = response.get('nextPageToken')

                # if token is None:
                #     break 
        except:
            pass
            


    return comments

#  getting playlist names
# getting playlist id,video id and title using playlistid(youtube) function
# input -- playlistId(youtube) here

def getPlaylistNames(youtube,df1):


    # df = getChannelStats(youtube, channel_name)
    # playlist_id= df['Playlist_Id']

    


    lis1=[]

    token = None
    while True:
    # for j in df1:

        request = youtube.playlistItems().list(
                    part="contentDetails,id,snippet,status",
                    playlistId= df1,
                    pageToken = token,
                    maxResults=50,
                    
        )
        response = request.execute()



        
        
        for i in range(len(response['items'])):
            
            # data = response['items'][i]['contentDetails']['videoId']
                data = dict(Channel_Id = response['items'][i]['snippet']['channelId'],
                            Playlist_Id = df1,
                            Video_Id = response['items'][i]['contentDetails']['videoId'],
                            Video_Name = response['items'][i]['snippet']['title'])

                lis1.append(data)

        token = response.get('nextPageToken')

        if token is None:
            break

    return lis1

def Overall(channel_name):
    c_id= channel(youtube, channel_name)
    # print(c_id)

    p_id = playlistId(youtube, c_id)
    # print(p_id)
    Playlist= videoId(youtube, p_id)
    # print("playlist : ",Playlist)

    channel_details= getChannelStats(youtube, c_id)
    # print(channel_details)
    cd=channel_details['Playlist_Id']
    # print(cd)

    Original=getPlaylistId(youtube,cd)
    # print("uploads : ",Original)

    final_video_id= videoIdFinal(Original,Playlist)
    # print("final : ",final_video_id)

    video_details= getVideoDetails(youtube,final_video_id,cd)
    # print(video_details)

    comment_details= getComment(youtube,final_video_id)
    # print(comment_details)

    playlist_Names= getPlaylistNames(youtube,cd)
    # print(playlist_Names)


    data = {"channel_data": channel_details,
            "video_details": video_details,
            "comment_details": comment_details,
            "playlist_Names": playlist_Names
            }
    
    return data

Overall_data = Overall('GamerOnofficial')

with open('file1.txt','w') as file:
    file.write(json.dumps(Overall_data))

# here we're inserting channels data into mongodb
def mongoDb(channel_name):

    Overall_data = Overall(channel_name)
    localClient, db, coll = MongoConnection()

    # inserting youtube data 
    coll.insert_one(Overall_data)

    return Overall_data

# Getting channel deails
# reading data from mongodb for all youtube channels

def MongoChannelData():
    localClient,db,coll = MongoConnection()
    lis1=[]
    # 
    for i in coll.find():
        lis1.append(i['channel_data'])
        # lis.append(i[''])
        # lis.append(i['playlist_Names'])
            
        
    return lis1
        

def ChannelDataToMySQL():
    db,mycursor = MyCursor()
    channel_data = pd.DataFrame(MongoChannelData())
    channel_data['Subscription_Count'] = channel_data['Subscription_Count'].astype(int)
    channel_data['Channel_views'] = channel_data['Channel_views'].astype(int)
    channel_data['video_Count'] = channel_data['video_Count'].astype(int)
    channel_data.dtypes
    channel_data

    # create table if not exists channel_data
    mycursor.execute("""create table if not exists channel_data (Channel_Name varchar(255), Channel_Id varchar(255) primary key not null, 
                 Subscription_Count int(255), Channel_views int(255), Channel_Description text, 
                 Playlist_Id varchar(255), video_Count int(255))""")
    
    # insert into channel_data
    sql = """INSERT INTO channel_data (Channel_Name,Channel_Id, Subscription_Count, Channel_views, 
    Channel_Description, Playlist_Id, video_Count) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    Channel_Name = VALUES(Channel_Name),Subscription_Count= VALUES(Subscription_Count), 
    Channel_views= VALUES(Channel_views), Channel_Description = VALUES(Channel_Description), 
    Playlist_Id = VALUES(Playlist_Id), video_Count= VALUES(video_Count)"""


    for i in channel_data.to_records().tolist():
        mycursor.execute(sql, i[1:])

    db.commit()
    mycursor.close()
    db.close()

# Getting Playlist table

def MongoPlaylistData():
    localClient,db,coll = MongoConnection()
    lis2=[]
    for i in coll.find():
        # print((i['video_details']))
        # print(i['playlist_Names'])
        # print(i['playlist_Names'])
    
        for j in range(len(i['playlist_Names'])):
            # print(j)
            data = dict(Channel_Id=[i][0]['playlist_Names'][j]['Channel_Id'],
                      Playlist_Id =[i][0]['playlist_Names'][j]['Playlist_Id'],
                      Video_Id = [i][0]['playlist_Names'][j]['Video_Id'],
                      Video_Name = [i][0]['playlist_Names'][j]['Video_Name'])
            lis2.append(data)
    
    return lis2

def PlaylistDataToMySQL():
    db, mycursor = MyCursor()
    playlist_data= pd.DataFrame(MongoPlaylistData())

    # creating table playlist_data if not exists
    mycursor.execute("""create table if not exists playlist_data (Channel_Id varchar(255), 
                    foreign key(Channel_Id) references channel_data(Channel_Id), 
                    Playlist_Id varchar(255),
                    Video_Id varchar(255) primary key,
                    Video_Name varchar(255))  """)

    # inserting into playlist_data
    sql = """INSERT INTO playlist_data (Channel_Id, 
            Playlist_Id, 
            Video_Id, 
            Video_Name) VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            Channel_Id = VALUES(Channel_Id),Playlist_Id = VALUES(Playlist_Id),Video_Name = VALUES(Video_Name)
            """
    # changing to tuple inside a list
    for i in playlist_data.to_records().tolist():
        mycursor.execute(sql,i[1:])

    db.commit()
    mycursor.close()
    db.close()

# Getting Video details 
def MongoVideoData():
    localClient,db,coll = MongoConnection()
    lis=[]
    for i in coll.find():

        for j in range(len(i['video_details'])):
            data = dict(Video_Id = [i][0]['video_details'][j]['Video_Id'],
                        Playlist_Id = [i][0]['video_details'][j]['Playlist_Id'],
                        Video_Name = [i][0]['video_details'][j]['Video_Name'],
                        Video_Description = [i][0]['video_details'][j]['Video_Description'],
                        PublishedAt = [i][0]['video_details'][j]['PublishedAt'],
                        View_Count = [i][0]['video_details'][j]['View_Count'],
                        Like_Count = [i][0]['video_details'][j]['Like_Count'],
                        Favorite_Count = [i][0]['video_details'][j]['Favorite_Count'],
                        Comment_Count = [i][0]['video_details'][j]['Comment_Count'],
                        Duration = [i][0]['video_details'][j]['Duration'],
                        Thumbnail = [i][0]['video_details'][j]['Thumbnail'],
                        Caption_Status = [i][0]['video_details'][j]['Caption_Status'])

            lis.append(data)
    
    return lis

def VideoDataToMySQL():
    db,mycursor = MyCursor()
    Video_Data = pd.DataFrame(MongoVideoData())

    Video_Data['PublishedAt'] = pd.to_datetime(Video_Data['PublishedAt'], unit='ns').dt.strftime('%Y-%m-%d %H:%M:%S')
    Video_Data['View_Count'] = Video_Data['View_Count'].astype('int64')
    Video_Data['Like_Count'] = Video_Data['Like_Count'].astype('int64')
    Video_Data['Favorite_Count'] = Video_Data['Favorite_Count'].astype('int64')
    Video_Data['Comment_Count'] = Video_Data['Comment_Count'].astype('int64')

    def duration_to_seconds(duration_str):
        duration = parse_duration(duration_str)
        return int(duration.total_seconds())

    Video_Data['Duration'] = Video_Data['Duration'].apply(duration_to_seconds)

    # create table if not exists video_data
    mycursor.execute("""create table if not exists video_data (Video_Id varchar(255) primary key,
                    Playlist_Id varchar(255),Video_Name varchar(255), Video_Description text, PublishedAt datetime,
                    View_Count bigint, Like_Count bigint, Favorite_Count bigint, Comment_Count bigint,
                    Duration bigint, Thumbnail varchar(255), Caption_Status varchar(255))""")

    # inserting into video_data
    sql = """insert into video_data (Video_Id, 
        Playlist_Id, 
        Video_Name, 
        Video_Description, 
        PublishedAt,
        View_Count,
        Like_Count,
        Favorite_Count,
        Comment_Count,
        Duration,
        Thumbnail,
        Caption_Status)
        values(%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        Playlist_Id = values(Playlist_Id), 
        Video_Name = values(Video_Name), 
        Video_Description= values(Video_Description), PublishedAt = values(PublishedAt),
        View_Count = values(View_Count), Like_Count = values(Like_Count), Favorite_Count = values(Favorite_Count),
        Comment_Count = values(Comment_Count), Duration = values(Duration), Thumbnail = values(Thumbnail),
        Caption_Status = values(Caption_Status)"""

    for i in Video_Data.to_records().tolist():
        mycursor.execute(sql,i[1:])

    db.commit()
    mycursor.close()
    db.close()

# Getting Comment Details
def MongoCommentData():
    localClient,db,coll = MongoConnection()
    lis3 = []
    for i in coll.find():
        # print(i['comment_details'])

        for j in range(len(i['comment_details'])):
            # print(j)
            data = dict(Comment_Id =i['comment_details'][j]['Comment_Id'] ,
                        Video_Id = i['comment_details'][j]['Video_Id'] ,
                        Comment_Text =i['comment_details'][j]['Comment_Text'] ,
                        Comment_Author =i['comment_details'][j]['Comment_Author'] ,
                        Comment_PublishedAt = i['comment_details'][j]['Comment_PublishedAt'] ,
                        Like_Count = i['comment_details'][j]['Like_Count'],
                        Reply_Count = i['comment_details'][j]['Reply_Count'])
            
            lis3.append(data)

    return lis3

def CommentDataToMySQL():
    db,mycursor = MyCursor()
    comment_data = pd.DataFrame(MongoCommentData())

    comment_data['Comment_PublishedAt'] = pd.to_datetime(comment_data['Comment_PublishedAt'], unit='ns').dt.strftime('%Y-%m-%d %H:%M:%S')

    # create table if not exists comment_data
    mycursor.execute("""create table if not exists comment_data (Comment_Id varchar(255) primary key,
                    Video_Id varchar(255),
                    foreign key(Video_Id) references video_data(Video_Id),
                    Comment_Text text, Comment_Author varchar(255),Comment_PublishedAt datetime, Like_Count int(255), 
                    Reply_Count int(255)) """)

    # inserting into comment data
    sql = """insert into comment_data (Comment_Id,
        Video_Id,
        Comment_Text,
        Comment_Author,
        Comment_PublishedAt,
        Like_Count,
        Reply_Count) values(%s ,%s ,%s ,%s ,%s ,%s,%s)
        ON DUPLICATE KEY UPDATE
        Video_Id = values(Video_Id),Comment_Text = values(Comment_Text),
        Comment_Author = values(Comment_Author), Comment_PublishedAt = values(Comment_PublishedAt),
        Like_Count = values(Like_Count), Reply_Count =values(Reply_Count)"""


    for i in comment_data.to_records().tolist():
        mycursor.execute(sql,i[1:])

    db.commit()
    mycursor.close()
    db.close()

def MigrateToMySQL():
    channel_data_sql = ChannelDataToMySQL()
    playlist_data_sql = PlaylistDataToMySQL()
    video_data_sql = VideoDataToMySQL()
    comment_data_sql = CommentDataToMySQL()

    return channel_data_sql, playlist_data_sql, video_data_sql, comment_data_sql

def Q1():
    db,mycursor = MyCursor()
    """	question 1
        What are the names of all the videos and their corresponding channels?"""

    mycursor.execute("""select c.channel_name, p.video_id,p.video_name from channel_data as c 
        inner join 
            playlist_data as p on c.channel_id = p.Channel_Id;""")
    
    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
    
    return df

def Q2():
	db,mycursor = MyCursor()
	"""	question 2
		select * from channel_data;
		Which channels have the most number of videos, and how many videos do
		they have?"""

	mycursor.execute("""select Channel_Name, video_Count from channel_data where video_Count 
	= (select max(video_Count) from channel_data);""")

	out = mycursor.fetchall()
	df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

	return df

def Q3():

	db,mycursor = MyCursor()
	"""	question 3
		What are the top 10 most viewed videos and their respective channels?"""

	mycursor.execute("""select channel_name, video_name,view_count, r
	from(
		select channel_name, video_name, view_count, rank() over(order by View_Count desc) as r
		from(
			select c.channel_name, v.video_name, v.view_count
			from channel_data as c
			inner join video_data as v on c.Playlist_Id=v.Playlist_Id
		)as x
	)as ranked_data
	where r<=10;""")

	out = mycursor.fetchall()
	df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
	
	return df

def Q4():
    db, mycursor = MyCursor()
    """	question 4
        set global sql_mode='';
        SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
        
        use youtube;
        select * from video_data;
        How many comments were made on each video, and what are their
        corresponding video names?"""

    mycursor.execute("""select Video_Name, Comment_Count from video_data order by Comment_Count desc;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df

def Q5():
    db, mycursor = MyCursor()
    """	question 5
        Which videos have the highest number of likes, and what are their 
        corresponding channel names?"""

    mycursor.execute("""select * from(
    select c.channel_name,v.video_id,v.video_name,v.Like_Count, row_number() over(partition by Channel_Name order by like_count desc) as r from channel_data as c
        inner join 
            video_data as v on v.playlist_id = c.playlist_id)as x
            where x.r =1;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df

def Q6():
    db,mycursor = MyCursor()
    """	question 6
        What is the total number of likes and dislikes for each video, and what are 
        their corresponding video names?"""

    mycursor.execute("""select video_name, like_count from video_data order by like_count desc;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df


def Q7():
    db,mycursor = MyCursor()
    """	question 7
        select * from channel_data;

        What is the total number of views for each channel, and what are their 
        corresponding channel names?"""

    mycursor.execute("""select channel_name, channel_views from channel_data order by Channel_views desc;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df

def Q8():
    db,mycursor = MyCursor()
    """	question 8
        What are the names of all the channels that have published videos in the year
        2022?"""

    mycursor.execute("""select c.channel_name, v.video_id,v.video_name, v.PublishedAt from channel_data as c
    inner join
        video_data as v 
        on v.Playlist_Id = c.Playlist_Id
        where year(v.publishedat) = 2022;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df


def Q9():
    db,mycursor = MyCursor()
    """question 9
        What is the average duration of all videos in each channel, and what are their 
        corresponding channel names?"""

    mycursor.execute("""select c.channel_name, c.Playlist_Id, v.Duration, row_number() over(partition by Playlist_Id order by duration desc) as r from channel_data as c
        inner join 
            video_data as v on c.Playlist_Id = v.Playlist_Id;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df

def Q10():
    db,mycursor = MyCursor()
    """question 10
        Which videos have the highest number of comments, and what are their 
        corresponding channel names?"""

    mycursor.execute("""select * from (
    select c.channel_name, v.video_name, v.comment_count, row_number() over(partition by channel_name order by comment_count desc) as r from channel_data as c
        inner join 
            video_data as v on c.playlist_id = v.playlist_id)as x
                where x.r=1;""")

    out = mycursor.fetchall()
    df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

    return df