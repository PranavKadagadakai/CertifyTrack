import io
import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile
from Cert.models import Event

def generate_certificates(event_id, participant_file_path, name_col="Name", usn_col="USN", horz=100, vert=500, font="Inter.ttf", font_size=24):
    try:
        # Fetch event and its certificate template from the database
        event = Event.objects.get(id=event_id)
        if not event.certificate_template:
            raise ValueError("No certificate template found for this event.")
        
        # Load the certificate template from binary field
        certemplate_binary = io.BytesIO(event.certificate_template)
        certemplate_binary.seek(0)
        existing_pdf = PdfReader(certemplate_binary)

        # Load the participant Excel file
        data = pd.read_excel(participant_file_path)
        name_list = data[name_col].tolist()
        usn_list = data[usn_col].tolist()

        # Ensure the certificates directory exists
        output_dir = os.path.join("certificates", f"event_{event.id}")
        os.makedirs(output_dir, exist_ok=True)

        # Register the font
        pdfmetrics.registerFont(TTFont("CustomFont", font))

        # Generate certificates
        for name, usn in zip(name_list, usn_list):
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Set the font and write the name and USN
            can.setFont("CustomFont", font_size)
            can.drawString(horz, vert, name.upper().strip())  # Name position
            can.drawString(horz, vert - 50, usn.upper().strip())  # USN position

            can.save()
            packet.seek(0)

            # Overlay the new content on the template
            new_pdf = PdfReader(packet)
            page = existing_pdf.pages[0]  # Use the first page of the template
            page.merge_page(new_pdf.pages[0])

            # Save the final certificate
            output = PdfWriter()
            output.add_page(page)
            cert_filename = os.path.join(output_dir, f"{name}_{usn}.pdf")
            with open(cert_filename, "wb") as outputStream:
                output.write(outputStream)
            
            print(f"Certificate created for {name} ({usn})")

        print("All certificates have been generated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
