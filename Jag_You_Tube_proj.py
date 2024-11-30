# You Tube Data Harvesting and Warehousing developed by Jagadeesh V
#  Nov. 2024
from googleapiclient.discovery import build
import mysql.connector
import streamlit as st
import re
from datetime import datetime
import pandas as pd

# YouTube Data API access
api_key = "AIzaSyCs0Yldqtu99WmMF-biPQUE6dhFflDIgGo"
youtube = build('youtube', 'v3',  developerKey=api_key)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Part 1 :  A. Functions for Data Extracting from You Tube data

# 1A1. Extract Channel data giving channel_id as parameter
def extract_channel_data(channel_id):
    try:
        channel_resp = youtube.channels().list(part="snippet,statistics,contentDetails", id=channel_id).execute()
        channel_snippet = channel_resp['items'][0]['snippet']
        channel_statistics = channel_resp['items'][0]['statistics']
        channel_contentDetails = channel_resp['items'][0]['contentDetails']
        return {
            'channel_name': channel_snippet['title'],
            'channel_ID': channel_id,
             'channel_type':  channel_resp['items'][0]['kind'],
            'Subscription_count': channel_statistics.get('subscriberCount', 0),
            'channel_views': channel_statistics.get('viewCount', 0),
            'channel_description': channel_snippet.get('description', ''),
            'Playlist_ID': channel_contentDetails.get('relatedPlaylists', {}).get('uploads', '')
        }
    except Exception as e:
        st.info('Invalid ID.  Either No such channel or Access forbidden')
        return {
            'channel_name': 'ERR',
            'channel_ID': channel_id,
             'channel_type':  "",
            'Subscription_count': 0,
            'channel_views': 0,
            'channel_description': '',
            'Playlist_ID': ''
        }

# 1A2. Extract Playlist_IDs of the YouTube channel using the playlist_id
def extract_Playlist_IDs(playlist_id):
    Playlist_IDs = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in playlist_response['items']:
            Playlist_IDs.append(item['snippet']['resourceId']['videoId'])
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break
    return Playlist_IDs

# 1A3. Extract details of all the videos in the YouTube channel using the Playlist_IDs
def extract_video_data(Playlist_ID):
    video_response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=Playlist_ID
    ).execute()
    video_snippet = video_response['items'][0]['snippet']
    video_statistics = video_response['items'][0]['statistics']
    video_content_details = video_response['items'][0]['contentDetails']
    time_string = video_content_details['duration']
    minutes = convert_to_minutes(time_string)
    return {
        'channel_ID': channel_id,
        'Playlist_ID': Playlist_ID,
        'Video_name': video_snippet['title'],
        'Video_description': video_snippet.get('description', ''),
        'Tags': video_snippet.get('tags', []),
        'Published_at': video_snippet['publishedAt'],
        'View_count': video_statistics.get('viewCount', 0),
        'Like_count': video_statistics.get('likeCount', 0),
        'Dislike_count': video_statistics.get('dislikeCount', 0),
        'Favorite_count': video_statistics.get('favoriteCount', 0),
        'Comment_count': video_statistics.get('commentCount', 0),
        'Duration': minutes,
        'Thumbnail': video_snippet['thumbnails']['default']['url'],
        'Caption_status': video_content_details['caption'],
        'Comments': []
    }

# 1A3a. Converting the Duration of the video in minutes PTnnthe data in database
def convert_to_minutes(time_string):
#    print(f"Time String : {time_string}")
    try:
        hour_match = re.match(r'PT(?P<hours>\d+)H(?P<minutes>\d+)M(?P<seconds>\d+)S', time_string)
        hour_min_match = re.match(r'PT(?P<hours>\d+)H(?P<minutes>\d+)M', time_string)
        min_sec_match = re.match(r'PT(?P<minutes>\d+)M(?P<seconds>\d+)S', time_string)
        hour_sec_match = re.match(r'PT(?P<hours>\d+)H(?P<seconds>\d+)S', time_string)
        hour_only_match = re.match(r'PT(?P<hours>\d+)H', time_string)
        minute_match = re.match(r'PT(?P<minutes>\d+)M', time_string)
        sec_match = re.match(r'PT(?P<seconds>\d+)S', time_string)
        
        if hour_match:
            hours = int(hour_match.group('hours'))
            minutes = int(hour_match.group('minutes'))
            seconds = int(hour_match.group('seconds'))
            return hours * 60 + minutes + seconds / 60
        elif hour_min_match:
            hours = int(hour_min_match.group('hours'))
            minutes = int(hour_match.group('minutes'))
            return hours * 60 + minutes
        elif min_sec_match:
            minutes = int(min_sec_match.group('minutes'))
            seconds = int(min_sec_match.group('seconds'))
            return minutes + seconds / 60
        elif hour_sec_match:
            hours = int(hour_sec_match.group('hours'))
            seconds = int(hour_sec_match.group('seconds'))
            return hours * 60 + seconds / 60
        elif hour_only_match:
            hours = int(hour_only_match.group('hours'))
            return hours * 60
        elif minute_match:
            minutes = int(minute_match.group('minutes'))
            return minutes
        elif sec_match:
            seconds = int(sec_match.group('seconds'))
            return seconds / 60
        else:
          raise ValueError('Invalid time string: {}'.format(time_string))
    except Exception as e:
        return 0

# 1A4. Extract the first 100 comments of each video in the YouTube channel using the Playlist_IDs
def extract_comments(Playlist_ID):
    try:
        comments = []
        next_page_token = None
        vid_stats = youtube.videos().list(
            part="statistics",
            id=Playlist_ID
        ).execute()
        comment_count = vid_stats.get("items")[0].get("statistics").get("commentCount")
        if comment_count != "None":
            while True:
                comment_response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=Playlist_ID,
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()
                for item in comment_response['items']:
                    comment_snippet = {'channel_ID': channel_id,
                                       'Playlist_ID': Playlist_ID,
                                       'Comment_text':item['snippet']['topLevelComment']['snippet']['textDisplay'],
                                       'Comment_ID':item['snippet']['topLevelComment']['id'],
                                       'Author_name':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                       'Published_at':item['snippet']['topLevelComment']['snippet']['publishedAt']
                                       }
                    comments.append(comment_snippet)
                next_page_token = comment_response.get('nextPageToken')
                if not next_page_token:
                    break
    except Exception as e:
        print(f"{Playlist_ID} has comments disabled, or  unknown Errors")
        comments.append({'channel_ID': channel_id,
                         'Playlist_ID': Playlist_ID,
                         'Comment_text':"has comments disabled, or  unknown Errors",
                         'Comment_ID':'0',
                         'Author_name':"",
                         'Published_at':""
                         })
    return comments

# 1B. Main.  Extract all the data of the YouTube channel(channel_data, Video_data, Comment_data) by calling the functions 1A1 to 1A4 above
def extract_data(channel_id):
    channel_data = extract_channel_data(channel_id)
    if channel_data['channel_name']  !=  'ERR':
        Playlist_IDs = extract_Playlist_IDs(channel_data['Playlist_ID'])
        video_data = []
        comment_data = []
        for Playlist_ID in Playlist_IDs:
            video_details = extract_video_data(Playlist_ID)
    #        print(video_details)
            video_details['Comments'] = extract_comments(Playlist_ID)
            video_data.append(video_details)
            comment_data.append(video_details['Comments'])
            video_df = pd.DataFrame(video_data)
            try:
                comment_df = pd.DataFrame(comment_data)
            except Exception as e:
                comment_df = pd.DataFrame([])
        return channel_data, video_df, comment_df
    else:
        return channel_data

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Part 2 : Inserting the extracted data in MySQL Database tables 

# 2A. Establishing MySql connection & DB
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "Sq!R00t")
mycursor = mydb.cursor(buffered = True)

#  ---------------------- To run only very first time (in case of new My Sql) -------------------- #
# 2B. Creating the DB & required Tables
mycursor.execute('create database if not exists YouTube_DB')   #--> To Run very first time only to create the DB
mycursor.execute('use YouTube_DB')
mycursor.execute('create table if not exists channels (channel_ID VARCHAR(255), channel_Name VARCHAR(255), channel_Type VARCHAR(255), channel_Views INT(15), channel_Description TEXT, channel_Status VARCHAR(255), Subscribers INT(50))')
mycursor.execute('create table if not exists videos (Video_ID VARCHAR(255), Video_Name VARCHAR(100), Video_Description TEXT, Published_Date DATETIME, View_count INT(20), Like_count INT(20), Dislike_count INT(20), Favorite_count INT(20), Comment_count INT(50), Duration VARCHAR(20), Thumbnail VARCHAR(255), Caption_Status VARCHAR(255), Channel_ID VARCHAR(100) )')
mycursor.execute('create table if not exists comments ( Comment_ID VARCHAR(255), Video_ID VARCHAR(255), Comment_Text TEXT,  Comment_Author VARCHAR(255), Comment_Published_Date DATETIME, channel_ID VARCHAR(255))')

# 2C. Insert the channel data, video data and comment data into SQL
def insert_data(channel_data, video_df):
    # 2C1. Insert channel data
    mycursor.execute("INSERT INTO channels (channel_name, channel_ID, Subscribers, channel_views, channel_description) VALUES (%s, %s, %s, %s, %s)",
                   (channel_data['channel_name'], channel_data['channel_ID'], channel_data['Subscription_count'], channel_data['channel_views'], channel_data['channel_description']))
    mydb.commit()

    # 2C2. Insert video data & Comments Data
    # 2C2a. inserting Video data
    for _, row in video_df.iterrows():
        try:
            mss_dt = datetime.strptime(row['Published_at'], "%Y-%m-%dT%H:%M:%SZ")
#            print(row['Playlist_ID'])
#        print(f"You Tube date : {row['Published_at']}")
#        print(ms_dt)
            mycursor.execute("INSERT INTO videos (channel_ID, Video_ID, Video_Name, Video_Description, Published_Date, view_count, like_count, Dislike_count, Favorite_count, Comment_count, Duration, Thumbnail, Caption_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (channel_data['channel_ID'], row['Playlist_ID'], row['Video_name'], row['Video_description'], mss_dt, row['View_count'], row['Like_count'], row['Dislike_count'], row['Favorite_count'], row['Comment_count'], row['Duration'], row['Thumbnail'], row['Caption_status']))
        except Exception as e:
            print("")
        mydb.commit()
    # 2C2b. inserting Comment data
        try:
            for comment in row['Comments']:
              mss_dt = datetime.strptime(comment['Published_at'], "%Y-%m-%dT%H:%M:%SZ")
              mycursor.execute("INSERT INTO comments (Comment_ID, Video_ID, Comment_text, Comment_Author, Comment_Published_Date, channel_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                              (comment['Comment_ID'], row['Playlist_ID'], comment['Comment_text'], comment['Author_name'], mss_dt, channel_data['channel_ID']))
        except Exception as e:
            print("")
        mydb.commit()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Main Streamlit routine to accept Channel ID, extract & Store Data and 10 queries
st.title(":red[YouTube] Data Harvesting and Warehousing")

mycursor.execute("SELECT COUNT(Channel_ID) AS channel_count FROM channels")
channel_count = mycursor.fetchone()[0]
mycursor.execute("SELECT COUNT(Video_ID) AS video_count FROM videos")
video_count = mycursor.fetchone()[0]
mycursor.execute("SELECT COUNT(Comment_ID) AS comment_count FROM comments")
comment_count =  mycursor.fetchone()[0]

st.subheader(r"$\textsf{\small Current data stored count }$")
#st.subheader(':blue[                                                                    Current data stored count]', anchor=None)
txt = {"Channels: ": [channel_count], "Videos: ": [video_count], "Comments: ":[comment_count]}
df = pd.DataFrame(data=txt)
st.table(df.style.background_gradient(cmap='Blues'))

channel_id = st.text_input("Enter YouTube Channel ID:")

def extract_insert_data_st():
    if st.button("Fetch & Store Data"):
            qry = "SELECT COUNT(Channel_ID) AS channel_count FROM channels where Channel_ID = '"+ channel_id +"'"
#            print(qry)
            mycursor.execute( qry)
            channel_count = mycursor.fetchone()[0]
            if channel_count == 0:
                channel_data, video_df, comment_df = extract_data(channel_id)
                if channel_data['channel_name']  !=  'ERR':
                    insert_data(channel_data, video_df)
                    st.success("Fetching & Storing data Completed")
                else:
                    st.info('Invalid Channel '+channel_id+ ' Rereival failed')
            else:
                st.info('Channel '+channel_id+ ' already retreived and stored')

extract_insert_data_st()

# Part 3 : Creating a streamlit application with the query of the questions given for the data stored in the local database
query_options = [
    " 1. Names of all the videos and their corresponding channels?",
    " 2. Channel having the most number of videos & its count",
    " 3. Top 10 most viewed videos and their channel Name",
    " 4. All comments and their video names",
    " 5. Video with highest number of likes and its channel name",
    " 6. No. of likes and dislikes of each Video with its name",
    " 7. No. of views for each channel with its name",
    " 8. List of Channels that have published videos in the year 2022",
    " 9. Average duration of all videos in each channel with their name",
    "10. Vidoe with highest No. of comments, and its channel name"
    ]
selected_query = st.selectbox("Select a query for result", query_options)

if st.button("Execute"):
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "Sq!R00t", database = "youtube_DB")
    if selected_query == query_options[0]:
        query_result = pd.read_sql_query("select Video_Name, Channel_Name from channels a, videos b where a.channel_id = b.channel_id order by Video_Name", mydb)
    elif selected_query == query_options[1]:
        #query_result = pd.read_sql_query("SELECT channel_Name, COUNT(Playlist_ID) AS Num_Videos FROM channels INNER JOIN videos ON channels.channel_ID = videos.channel_ID GROUP BY channel_Name ORDER BY Num_Videos DESC LIMIT 1", mydb)
        query_result = pd.read_sql_query("select channel_Name, count(video_id) as No_of_Videos from channels a, videos b where a.channel_id = b.channel_id group by channel_Name order by count(video_id) desc limit 1", mydb)
    elif selected_query == query_options[2]:
        query_result =pd.read_sql_query("select  Video_Name, View_count as Views, Channel_Name from channels a, videos b where a.channel_id = b.channel_id order by view_count desc limit 10;", mydb)
    elif selected_query == query_options[3]:
        query_result = pd.read_sql_query("Select Video_Name, COUNT(Comment_ID) as No_of_Comments from videos b, comments c where b.Video_ID = c.Video_ID group by Video_Name order by Video_name;", mydb)
    elif selected_query == query_options[4]:
        query_result = pd.read_sql_query("Select Video_Name, channel_Name, like_count as No_of_Likes from channels a, videos b where b.channel_ID = a.channel_ID order by like_count Desc Limit 1;", mydb)
    elif selected_query == query_options[5]:
        query_result = pd.read_sql_query("Select Video_Name, Sum(like_count) as Total_Likes, Sum(Dislike_count) as Total_Dislikes from  videos group by Video_Name order by video_name;", mydb)
    elif selected_query == query_options[6]:
        query_result = pd.read_sql_query("Select channel_Name, Sum(View_Count) as Total_Views From channels a, videos b where a.channel_ID = b.channel_ID group by channel_Name order by channel_Name;", mydb)
    elif selected_query == query_options[7]:
        query_result = pd.read_sql_query("Select channel_Name, count(b.channel_ID) as No_of_Videos From channels a, Videos b Where a.channel_ID = b.channel_ID and Year(b.Published_Date) = '2022' Group by channel_Name;", mydb)
    elif selected_query == query_options[8]:
        query_result = pd.read_sql_query("Select channel_Name, Round(Avg(Duration), 2) as Average_Duration From channels a, Videos b where b.channel_ID = a.channel_ID Group by channel_Name;", mydb)
    elif selected_query == query_options[9]:
        query_result = pd.read_sql_query("Select b.Video_Name, a.channel_Name, b.comment_count as No_of_comments from Channels a, videos b where a.channel_ID = b.Channel_ID order by Comment_count Desc Limit 1;", mydb)
    mydb.close()

    st.dataframe(query_result)
