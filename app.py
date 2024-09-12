import streamlit as st
from title import create_title_page
from copywright import create_copyright_page
from others import get_response_o, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers
from Glossary import get_response_g, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers
from author_praise import get_response_a, save_response
import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

os.system('playwright install')

# Create a ThreadPoolExecutor to run the async function
executor = ThreadPoolExecutor()

# Function to convert HTML to PDF with Playwright
nest_asyncio.apply()

async def html_to_pdf_with_margins(html_file, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        await page.set_content(html_content, wait_until='networkidle')

        pdf_options = {
            'path': output_pdf,
            'format': 'A4',
            'margin': {
                'top': '85px',
                'bottom': '60px',
                'left': '70px',
                'right': '60px'
            },
            'print_background': True
        }

        await page.pdf(**pdf_options)
        await browser.close()

st.title("Book Preliminary Pages PDF Generator")

# Page selection
page_type = st.selectbox("Select the type of page to create", 
                         ["Title Page", "Copyright Page", "Glossary", "Author's Praise", "Blank Page", "Others"])

# Conditional inputs based on page type
if page_type == "Title Page":
    title = st.text_input("Book Title")
    subtitle = st.text_input("Subtitle")
    author = st.text_input("Author Name")
    
    font_name = st.selectbox("Select Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    title_size = st.slider("Title Font Size", 24, 72, 48)
    subtitle_size = st.slider("Subtitle Font Size", 18, 36, 28)
    author_size = st.slider("Author Name Font Size", 12, 36, 24)
    
    if st.button("Create Title Page"):
        pdf_bytes = create_title_page(title, subtitle, author, font_name, title_size, subtitle_size, author_size)
        st.download_button("Download PDF", pdf_bytes, file_name="title_page.pdf")

elif page_type == "Copyright Page":
    
    author_name = st.text_input("Enter the Author's Name")
    typesetter_name = st.text_input("Enter the Typesetter's Name")
    printer_name = st.text_input("Enter the Printer's Name")
    font_size = st.text_input('Enter the Font Size')
    output_pdf = "copywright.pdf"
    if st.button("Create Copyright Page"):
        create_copyright_page(author_name, typesetter_name, printer_name, output_pdf, font_size)   
        with open(output_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Copywright PDF",
                data=pdf_file,
                file_name=output_pdf,
                mime="application/pdf"
            )

elif page_type == "Others":
    text = st.text_area("Enter the text")
    author_name = st.text_input('Enter the Author Name:')
    book_name = st.text_input('Enter the Book Name:')
    
    # Font options for body text
    body_font_name = st.selectbox("Select Body Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    body_font_size = st.text_input('Enter the Body Font Size')

    # Font options for header text
    header_font_name = st.selectbox("Select Header Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    header_font_size = st.text_input('Enter the Header Font Size')
    
    first_page_no = st.number_input('Enter the First Page Number:', min_value=0, max_value=1000, step=1)
    options = ['Left', 'Right']
    first_page_position = st.selectbox('Select First Page Position:', options)
    
    if st.button("Create Page"):
        response = get_response_o(text, body_font_size, body_font_name, header_font_name, header_font_size)
        html_pth = save_response(response)
        main_pdf = 'other.pdf'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf))
        
        total_pages = get_pdf_page_count(main_pdf)
        overlay_pdf = "overlay.pdf"

        create_overlay_pdf(overlay_pdf, total_pages, first_page_no, book_name, author_name, body_font_name, first_page_position)
        
        final_pdf = 'final.pdf'

        # Overlay the headers and footers
        overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)
        
        with open(final_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=final_pdf,
                mime="application/pdf"
            )

elif page_type == "Glossary":
    text = st.text_area("Enter the text")
    author_name = st.text_input('Enter the Author Name:')
    book_name = st.text_input('Enter the Book Name:')
    
    # Font options for body text
    body_font_name = st.selectbox("Select Body Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    body_font_size = st.text_input('Enter the Body Font Size')

    # Font options for header text
    header_font_name = st.selectbox("Select Header Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    header_font_size = st.text_input('Enter the Header Font Size')
    
    first_page_no = st.number_input('Enter the First Page Number:', min_value=0, max_value=1000, step=1)
    options = ['Left', 'Right']
    first_page_position = st.selectbox('Select First Page Position:', options)
    
    if st.button("Create Glossary Page"):
        response = get_response_g(text, body_font_size, body_font_name, header_font_name, header_font_size)
        html_pth = save_response(response)
        main_pdf = 'glosary.pdf'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf))
        
        total_pages = get_pdf_page_count(main_pdf)
        overlay_pdf = "overlay.pdf"

        create_overlay_pdf(overlay_pdf, total_pages, first_page_no, book_name, author_name, body_font_name, first_page_position)
        
        final_pdf = 'final.pdf'

        # Overlay the headers and footers
        overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)
        
        with open(final_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Glossary PDF",
                data=pdf_file,
                file_name=final_pdf,
                mime="application/pdf"
            )
    
elif page_type == "Author's Praise":
    text = st.text_area("Enter the text")
    
     # Font options for body text
    body_font_name = st.selectbox("Select Body Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    body_font_size = st.text_input('Enter the Body Font Size')

    # Font options for header text
    header_font_name = st.selectbox("Select Header Font", ["Helvetica", "Helvetica-Bold", "Courier", "Times-Roman"])
    header_font_size = st.text_input('Enter the Header Font Size')
    
    if st.button("Create Authors Praise Page"):
        response = get_response_a(text, body_font_size, body_font_name, header_font_name, header_font_size)
        html_pth = save_response(response)
        main_pdf = 'authors_praise.pdf'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf))
        
        with open(main_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=main_pdf,
                mime="application/pdf"
            )

elif page_type == "Blank Page":
    st.write("This will generate a blank page in the PDF.")
    
    if st.button("Create Blank Page"):
        
        blank_pdf = "blank_page.pdf"
        c = canvas.Canvas(blank_pdf, pagesize=A4)
        
        c.showPage()  # Finalize the page
        c.save()
        
        # Allow the user to download the blank page
        with open(blank_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Blank Page PDF",
                data=pdf_file,
                file_name="blank_page.pdf",
                mime="application/pdf"
            )
