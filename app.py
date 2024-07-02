import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
#get text detail form yt
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    




#get summary from ai
genai.configure(api_key=os.getenv("Google_api_key"))
prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """
def generate_containt(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(transcript_text+prompt)
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_containt(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

