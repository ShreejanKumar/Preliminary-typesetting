import os
import streamlit as st
from openai import OpenAI

def get_response_a(chapter, body_font_size, body_font_name, header_font_name, header_font_size):
  
    # Set up OpenAI API client
    api_key = st.secrets["Openai_api"]
    client = OpenAI(
        # This is the default and can be omitted
        api_key = api_key
       )

    # Set up OpenAI model and prompt
    model="gpt-4o-mini-2024-07-18"
    prompt_template = """
  You’re a skilled Editor and HTML expert with extensive experience in creating well-structured and visually appealing HTML documents. Your specialty lies in converting text into clean, semantic HTML while ensuring that the output is easy to read and maintain.

Your task is to generate an HTML file based on the text I provide. Here are the details you need to consider:
- Text: <<CHAPTER_TEXT>>
- font_size for body text: <<body_font_size>>
- font_name for body text: <<body_font_name>>
- font_size for header text: <<header_font_size>>
- font_name for header text: <<header_font_name>>
- Do not write anything else like ```html in the response, directly start with the doctype line.
- Do not add any extra text or headings other than what is being provided.
- The Heading which is provided should be centred and leave some space from the top of the page.
- This will be an authors praise page. The text will be quotes said by other people. The text should be written in double quotes and the name of the person should be written below in bold aligned to the right side. The text should be written normally withoutany additional formatting.
- The alignment of the text should be justified.
Please ensure that the generated HTML document includes appropriate tags for the title, headings, paragraphs, and any necessary metadata, making it ready for web display. It's important to maintain proper indentation and include comments for clarity.
    """
    prompt = prompt_template.replace("<<CHAPTER_TEXT>>", chapter).replace("<<body_font_size>>", body_font_size + "px").replace("<<body_font_name>>", body_font_name).replace("<<header_font_size>>", header_font_size + "px").replace("<<header_font_name>>", header_font_name)
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        temperature = 0
        )

    response = chat_completion.choices[0].message.content
    return response
        
        
def save_response(response):
        html_pth = 'neww.html'
        with open(html_pth, 'w', encoding='utf-8') as file:
            file.write(response)
        return html_pth


def get_pdf_page_count(pdf_file):
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages)


