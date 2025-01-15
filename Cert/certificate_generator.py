import io
import base64
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_image_certificate(template, participant_name, usn=None):
    """
    Generate a certificate image by overlaying participant details.
    """
    with Image.open(io.BytesIO(template)) as img:
        draw = ImageDraw.Draw(img)
        # Font configuration (adjust path and size as necessary)
        font = ImageFont.truetype("arial.ttf", 40)
        
        # Positioning for text (adjust coordinates for your template)
        draw.text((300, 200), participant_name, font=font, fill="black")
        if usn:
            draw.text((300, 250), usn, font=font, fill="black")
        
        # Save the result in binary format
        output = io.BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()

def generate_pdf_certificate(template, participant_name, usn=None):
    """
    Generate a certificate PDF by overlaying participant details.
    """
    output = io.BytesIO()
    template_io = io.BytesIO(template)

    # Create a new PDF and overlay participant details
    c = canvas.Canvas(output, pagesize=letter)
    c.drawImage(template_io, 0, 0, width=letter[0], height=letter[1])

    # Add participant details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 300, f"Name: {participant_name}")
    if usn:
        c.drawString(200, 270, f"USN: {usn}")

    c.save()
    return output.getvalue()

def generate_certificate(template, participant_name, usn=None, file_type="pdf"):
    """
    Generate a certificate based on the template file type.
    """
    if file_type in ["png", "jpg", "jpeg"]:
        return generate_image_certificate(template, participant_name, usn)
    elif file_type == "pdf":
        return generate_pdf_certificate(template, participant_name, usn)
    else:
        raise ValueError(f"Unsupported template file type: {file_type}")

if __name__ == "__main__":
    print("Hello!")
    temp_file_path: str = "/home/pranav/Downloads/Temp/template.pdf"
    participant_name: str = "PRANAV S KADAGADAKAI"
    
    generate_certificate(template=temp_file_path, participant_name=participant_name)   