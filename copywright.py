from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

def create_copyright_page(author_name, typesetter_name, printer_name, press_name, year, isbn, output_pdf, font_size):
    # Create a document with A4 size
    pdf = SimpleDocTemplate(output_pdf, pagesize=A4)
    
    # Set up styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontSize = int(font_size)
    normal_style.leading = 14  # Adjust line spacing
    center_style = ParagraphStyle('Center', parent=styles['Normal'], fontSize=int(font_size), leading=14, alignment=TA_CENTER)  # Center alignment

    # List to hold the PDF elements
    content = []
    if press_name == "Nu Voice Press":
        # Add the image
        logo = Image("Screenshot (53).png")  # Adjust as needed
        logo.hAlign = 'LEFT'
        content.append(logo)
        content.append(Spacer(1, 12))
        
        # Add the text
        text_content = [
            f"Copyright © {author_name} {year}",
            "",
            "The moral rights of the author have been asserted <br/> Database right NU VOICE PRESS (maker)",
            "",
            "This is a work of fiction and all characters and incidents <br/> described in this book are the product of the author's <br/> imagination. Any resemblance to actual persons, living or dead, <br/> is entirely coincidental.",
            "",
            "All rights reserved. Enquiries concerning reproduction outside <br/> the scope of the above should be sent to NU VOICE PRESS <br/> at the address above.",
            "",
            f"ISBN: {isbn}",
            "",  # Add a spacer after the ISBN line
            f"Typeset by {typesetter_name}, Noida",
            f"Printed at {printer_name}",
            "Published by Nu Voice Press"
        ]
    
        for paragraph in text_content:
            content.append(Paragraph(paragraph, normal_style))
            content.append(Spacer(1, 12))  # Add space between paragraphs
    
        # Build the PDF
        pdf.build(content)
    
    else:
        content.append(Spacer(1, 150))  # Adjust the value (e.g., 30) to set the desired space
        # Add the image
        logo = Image("Screenshot (57).png")  # Adjust as needed
        logo.hAlign = 'CENTER'
        content.append(logo)
        content.append(Spacer(1, 50))

        # Add the text
        text_content = [
            f"This edition is published by Solomon Press {year}",
            "",
            "Unit-125, First floor, Vipul Trade Centre, Sector-48, Sohna Road, South City-2 Gurugram, Haryana,122018",
            "", "",

            f"ISBN: {isbn}",
            "", "",  # Add a spacer after the ISBN line
            f"Typeset by {typesetter_name}, Noida",
            "Processed and Printed in India",
        ]

        for paragraph in text_content:
            content.append(Paragraph(paragraph, center_style))
            content.append(Spacer(1, 12))  # Add space between paragraphs
    
        # Build the PDF
        pdf.build(content)
