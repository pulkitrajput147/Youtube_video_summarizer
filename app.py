# Importing Necessary Libraries
import streamlit as st
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os

# Loading all the environment variables
load_dotenv()

# Access the API key
api_key = os.getenv("GOOGLE_API_KEY")

# configure the genai
genai.configure(api_key=api_key)

# Defining prompt
prompt="""
        You are an Expert Youtube Video Summarizer.You will take the transcript text and summarize
        the entire transcript text in detail, so that it doesn't miss out important details and provide the whole
        summary in points.The Transcript text is here :

"""

# getting the transcript data from youtube video
def extract_transcript(Video_link):
  try:
    video_id = Video_link.split("=")[1]
    transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

    transcript=""

    for i in transcript_text:
      transcript += " " +i["text"]

    return transcript

  except Exception as e:
    raise e

# Getting the summary out of transcript data
def generate_response(transcript_text,prompt):
  model=genai.GenerativeModel('gemini-pro')
  response=model.generate_content(prompt+transcript_text)
  return response.text


# creating user interface via streamlit
st.title(" Youtube Video Summarizer")
video_link=st.text_input("Enter the youtube Video Link")

if video_link:
  video_id=video_link.split("=")[1]
  st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg',use_column_width=True)

if st.button("Get Detailed Notes"):
  transcript_text=extract_transcript(video_link)

  if transcript_text:
    summary= generate_response(transcript_text,prompt)
    st.markdown("Detailed Notes :")
    st.write(summary)