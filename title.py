from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch 
from io import BytesIO
from reportlab.platypus import Image

def create_title_page(title, subtitle, author, font_name="Helvetica", title_size=36, subtitle_size=24, author_size=18):
    # Create a buffer to store the PDF
    buffer = BytesIO()
    
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Customize the font styles
    title_style = ParagraphStyle(
        name='Title',
        fontName=font_name,
        fontSize=title_size,
        alignment=1,  # Centered
        spaceAfter=0.5*inch
    )
    
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontName=font_name,
        fontSize=subtitle_size,
        alignment=1,  # Centered
        spaceAfter=0.5*inch
    )
    
    author_style = ParagraphStyle(
        name='Author',
        fontName=font_name,
        fontSize=author_size,
        alignment=1,  # Centered
    )
    
    # Build the content for the PDF
    content = []
    content.append(Spacer(1, 2*inch))
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 0.75*inch))
    content.append(Paragraph(subtitle, subtitle_style))
    content.append(Spacer(1, 1*inch))
    content.append(Paragraph(author, author_style))
    content.append(Spacer(1, 2.25*inch))
    
    # Add image at the end
    img = Image("NU_Voice_Black.png", width=2*inch, height=2*inch)
    content.append(img)

    # Build the PDF and save it to the buffer
    pdf.build(content)
    
    # Get the PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
