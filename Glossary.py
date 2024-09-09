import os
import streamlit as st
from openai import OpenAI

def get_response_g(chapter, font_size, font_name):
  
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
- font_size: <<fontsize>>
- font_name: <<fontname>>
- Do not write anything else like ```html in the response, directly start with the doctype line.
- Do not add any extra text or headings other than what is being provided
- The Heading should be centred and leave some space from the top of the page
- This will be a glossary page so for each item the word before the colon should be bold and italicised.
- The text should be left aligned.
Please ensure that the generated HTML document includes appropriate tags for the title, headings, paragraphs, and any necessary metadata, making it ready for web display. It's important to maintain proper indentation and include comments for clarity.

"""
  prompt = prompt_template.replace("<<CHAPTER_TEXT>>", chapter).replace("<<fontsize>>", font_size + "px").replace("<<fontname>>", font_name)
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

def create_overlay_pdf(overlay_pdf, total_pages, starting_page_number, book_name, author_name, font, first_page_position="Right"):
    c = canvas.Canvas(overlay_pdf, pagesize=A4)
    width, height = A4

    def draw_header_footer(page_number, position):
        c.setFont(font, 12)

        if page_number == starting_page_number:
            # First page of the chapter: Draw page number at the bottom center
            footer_y = 30  # Adjust this value to match the bottom text's baseline
            c.drawCentredString(width / 2, footer_y, f'{page_number}')
        elif position == "Right":
            # Right-side pages: Draw header on the right and page number at the right
            c.drawCentredString(width / 2, height - 40, book_name)
            c.drawString(width - 84, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap
        elif position == "Left":
            # Left-side pages: Draw header on the left and page number at the left
            c.drawCentredString(width / 2, height - 40, author_name)
            c.drawString(62, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap

    # Set the initial position based on the first_page_position
    current_position = first_page_position

    # Create pages for the overlay
    for i in range(total_pages):
        current_page_number = starting_page_number + i  # Continuous page numbering
        draw_header_footer(current_page_number, current_position)

        # Alternate position for the next page
        current_position = "Left" if current_position == "Right" else "Right"

        c.showPage()

    c.save()

def overlay_headers_footers(main_pdf, overlay_pdf, output_pdf):
    pdf_writer = PdfWriter()

    # Load the main PDF and the overlay PDF
    with open(main_pdf, 'rb') as main_file, open(overlay_pdf, 'rb') as overlay_file:
        main_pdf_reader = PdfReader(main_file)
        overlay_pdf_reader = PdfReader(overlay_file)

        # Ensure the overlay PDF has the same number of pages as the main PDF
        print(len(overlay_pdf_reader.pages))
        print(len(main_pdf_reader.pages))
        if len(overlay_pdf_reader.pages) != len(main_pdf_reader.pages):
            raise ValueError("The number of pages in the overlay PDF does not match the number of pages in the main PDF.")

        # Overlay headers and footers on each page
        for page_num in range(len(main_pdf_reader.pages)):
            main_page = main_pdf_reader.pages[page_num]
            overlay_page = overlay_pdf_reader.pages[page_num]

            # Merge the overlay onto the main page
            main_page.merge_page(overlay_page)

            pdf_writer.add_page(main_page)

    # Write the combined PDF to the output file
    with open(output_pdf, 'wb') as outfile:
        pdf_writer.write(outfile)