from youtube_transcript_api import YouTubeTranscriptApi as yta # type: ignore
import streamlit as st # type: ignore
from fpdf import FPDF # type: ignore
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
        L = [link1, link2, link3, link4, link5]
        store_videos_transcript(L)

    st.text_input("Read-only Text Input", value="This is read-only", disabled=True)

def store_videos_transcript(links):
    pattern = re.compile(r'(?<=v=)[\w-]+')
    for link in links:
        match = pattern.search(link)
        if match:
            v_value = match.group(0)
            try:
                data = yta.get_transcript(v_value)
                # Store transcript in a file named after the link
                filename = f"text_files/{v_value}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    for entry in data:
                        file.write(entry['text'] + "\n")
                st.success(f"Transcript for video {v_value} saved to {filename}")
            except Exception as e:
                st.error(f"Failed to retrieve transcript for video {v_value}: {str(e)}")
        else:
            st.error(f"No YouTube video ID found in {link}")
    pdf_generation()

def pdf_generation():
    text_files = os.listdir('./text_files')
    pdf = FPDF()
    for i in text_files:
        with open(f'text_files/{i}','r') as file:
            text = file.read()
        pdf.add_page()
        # Set font for the PDF
        pdf.set_font("Arial", size=12)
        # Add the text to the PDF
        pdf.multi_cell(0, 10, txt=text)
    
    pdf_output = "generated_pdf/transcripts.pdf"
    pdf.output(pdf_output)
    st.success("PDF generated successfully")

def generate_script(pdf):
    st.success("")

if __name__ == "__main__":
    main()
