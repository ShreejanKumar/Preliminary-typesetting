from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.platypus import Image

def create_title_page(title, subtitle, author, press_name, font_name="Helvetica", title_size=36, subtitle_size=24, author_size=18):
    # Create a buffer to store the PDF
    buffer = BytesIO()
    
    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Define maximum width for text wrapping
    max_title_width = 6.5 * inch
    
    # Create the title style
    title_style = ParagraphStyle(
        name='Title',
        fontName=font_name,
        fontSize=title_size,
        alignment=1,  # Centered
        spaceAfter=0.5*inch,
        leading=title_size + 5  # Ensure line spacing prevents overlap
    )
    
    # Adjust title size dynamically if it exceeds the width
    while True:
        title_paragraph = Paragraph(title, title_style)
        width, height = title_paragraph.wrap(max_title_width, 0)  # Wrap the title
        if height <= 2 * inch:
            break
        title_style.fontSize -= 2  # Reduce font size
        title_style.leading = title_style.fontSize + 5  # Adjust line spacing
    
    # Define subtitle and author styles
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
    content.append(Spacer(1, 1.5 * inch))  # Add some top margin
    content.append(title_paragraph)
    content.append(Spacer(1, 0.5 * inch))
    content.append(Paragraph(subtitle, subtitle_style))
    content.append(Spacer(1, 1 * inch))
    content.append(Paragraph(author, author_style))
    content.append(Spacer(1, 1.5 * inch))
    
    # Add the press-specific image
    if press_name == "Nu Voice Press":
        img = Image("NU_Voice_Black.png", width=2*inch, height=2*inch)
    else:
        img = Image("Screenshot (57).png", width=1*inch, height=1*inch)
    content.append(img)
    
    # Build the PDF and save it to the buffer
    pdf.build(content)
    
    # Get the PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
