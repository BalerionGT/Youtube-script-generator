from youtube_transcript_api import YouTubeTranscriptApi as yta
import streamlit as st
import re
import os

def main():
    st.title('▶ Welcome to the YouTube Script Generator')
    link1 = st.text_input('Enter link 1')
    link2 = st.text_input('Enter link 2')
    link3 = st.text_input('Enter link 3')
    link4 = st.text_input('Enter link 4')
    link5 = st.text_input('Enter link 5')

    if st.button('Generate'):
        store_videos_transcript(link1, link2, link3, link4, link5)

def store_videos_transcript(*links):
    pattern = re.compile(r'(?<=v=)[\w-]+')
    for link in links:
        match = pattern.search(link)
        if match:
            v_value = match.group(0)
            try:
                data = yta.get_transcript(v_value)
                # Store transcript in a file named after the link
                filename = f"{v_value}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    for entry in data:
                        file.write(entry['text'] + "\n")
                st.success(f"Transcript for video {v_value} saved to {filename}")
            except Exception as e:
                st.error(f"Failed to retrieve transcript for video {v_value}: {str(e)}")
        else:
            st.error(f"No YouTube video ID found in {link}")

if __name__ == "__main__":
    main()
