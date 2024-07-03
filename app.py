import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Directly include the Gemini API key
GEMINI_API_KEY = "AIzaSyBnMQZf2g3fLoXYg66R2gXSXtO-6TEf5Tw"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to extract transcript details from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

# Function to get a summary from the AI
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def generate_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(transcript_text + prompt)
    return response.text

# Streamlit app interface
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
