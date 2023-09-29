import streamlit as st
from youtube_api_version_2 import Overall
from youtube_api_version_2 import mongoDb
from youtube_api_version_2 import MigrateToMySQL
# from youtube_api_version_2 import ChannelDataToMySQL
# from youtube_api_version_2 import PlaylistDataToMySQL
# from youtube_api_version_2 import VideoDataToMySQL
# from youtube_api_version_2 import CommentDataToMySQL
from youtube_api_version_2 import Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10
# from youtube_api_version_2 import MyCursor

# title and description
# st.title("Youtube Channel Data Analysis")
# st.write("Enter the youtube channel name to get analysis details")

st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <h1 style="font-size: 30px; color: #808000">Youtube Channel Data Analysis</h1>
    </div>
    <div style="display: flex; justify-content: center;">
        <h1 style="font-size: 15px; color: #FFD700">Enter the YouTube channel name to get analysis details</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# user input field
# channel_name = st.text_input("Enter Youtube Channel Name")


with st.container():
    # st.title("Container Example")
    # st.write("this is the content inside the container")


    col1, col2 = st.columns(2)

    with col1:
        channel_name = st.text_input("Enter Youtube Channel Name to Read")
        # Content for the first column

        if channel_name:
            if st.button("ReadData"):
                try:
                    # call your overall function with user input
                    result = Overall(channel_name)

                    # Display the result using Streamlit
                    st.write("Channel Data:")
                    st.write(result["channel_data"])
                    
                    st.write("Video Details:")
                    # st.write(result["video_details"])
                    
                    st.write("Comment Details:")
                    # st.write(result["comment_details"])
                    
                    st.write("Playlist Names:")
                    # st.write(result["playlist_Names"])
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


    with col2:
        # Content for the second column
        insertchannel_name = st.text_input("Enter youtube Channel Name To Write")

        if insertchannel_name:
            if st.button("InsertToMONGOdb"):
                try:
                    data = mongoDb(insertchannel_name)

                    st.success("Data saved to Mongo db")
                    # st.write(data)
                except Exception as e:
                    st.error(f"An error occured : {str(e)}")


# st.write("This is content outside container")

with st.container():

    st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <h1 style="font-size: 15px; color: #FFD700">Migration From MongoDb to MySQL</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

    if st.button('MigrateTOMySQL'):
        try:
            data = MigrateToMySQL()
            st.success("MongoDb toMySQL Migration Succeeded")
        
        except Exception as e:
            print(f"An error occured : {str(e)}")


questions = {
    "1 names of all the videos and their corresponding channels":Q1,
    "2 Which channels have the most number of videos, and how many videos do they have":Q2,
    "3 top 10 most viewed videos and their respective channels":Q3,
    "4 How many comments were made on each video":Q4,
    "5 Which videos have the highest number of likes":Q5,
    "6 What is the total number of likes and dislikes ":Q6,
    "7 the total number of views for each channel":Q7,
    "8 channels that have published videos in the year 2022":Q8,
    "9 average duration of all videos in each channel":Q9,
    "10 Which videos have the highest number of comments":Q10
}

#  questionarie section dropdown list
with st.container():


    option = st.selectbox(
        'SQL Query Output need to displayed as table in Streamlit Application:',
        (
         list(questions.keys())
         ))
    
    if option in questions:
        st.write('Your Selected Option:', option)

        # Execute selected question and display as a result
        result = questions[option]()
        st.dataframe(result, use_container_width=True)

        if result.empty:
            st.write("No Data available for this query")