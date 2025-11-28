import os
import json
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from django.conf import settings


class CertificateGenerator:
    """
    Generates PDF certificates using:
    - A background PNG template (AICTE or Regular)
    - A JSON metadata file with coordinates
    - Dynamic text (name, event, date, etc.)
    - Dynamic signature images (faculty + principal)
    - QR code for verification3
    """

    def __init__(self, template_path, metadata_path):
        self.template_path = template_path
        self.metadata_path = metadata_path
        self.template_dir = os.path.dirname(template_path)

    def load_metadata(self):
        """Load JSON metadata (coordinates, font sizes, signature positions)"""
        with open(self.metadata_path, "r") as f:
            return json.load(f)

    def generate_qr_code(self, qr_text):
        """Generate QR code PNG in memory"""
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def draw_text(self, c, text, meta):
        """Draws text on PDF canvas at given coordinates."""
        c.setFont(meta["font"], meta["font_size"])
        c.drawString(meta["x"], meta["y"], text)

    def draw_image(self, c, image_path, meta):
        """Draws an image (signature, QR code, template)."""
        if not os.path.exists(image_path):
            return  # fail silently if signature not uploaded
        img = ImageReader(image_path)
        c.drawImage(
            img,
            meta["x"],
            meta["y"],
            width=meta["width"],
            height=meta["height"],
            preserveAspectRatio=True,
            mask="auto",
        )

    def generate_certificate(
        self,
        template_type,  # "certificate_aicte" or "certificate_regular"
        student_name,
        event_name,
        club_name,
        date,
        usn,
        points,  # ignored if regular cert
        qr_text,
        faculty_signature_path,
        principal_signature_path,
    ):
        """
        Generate certificate and return BytesIO buffer
        """
        from io import BytesIO
        metadata = self.load_metadata()

        # PDF canvas (A4 Landscape) - use BytesIO buffer
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))

        # Background template PNG
        template_png = self.template_path
        c.drawImage(template_png, 0, 0, width=A4[1], height=A4[0])  # A4 landscape

        # Draw text placeholders
        placeholders = metadata["placeholders"]

        self.draw_text(c, student_name, placeholders["student_name"])
        self.draw_text(c, event_name, placeholders["event_name"])
        self.draw_text(c, club_name, placeholders["club_name"])
        self.draw_text(c, date, placeholders["date"])
        self.draw_text(c, usn, placeholders["usn"])

        # AICTE points field only for AICTE template
        if template_type == "certificate_aicte":
            self.draw_text(c, str(points), placeholders["points"])

        # Generate QR Code (in-memory)
        qr_image = self.generate_qr_code(qr_text)
        qr_path = os.path.join(self.template_dir, "qr_temp.png")
        qr_image.save(qr_path)

        # Draw QR code
        self.draw_image(c, qr_path, metadata["qrcode"])

        # Draw signatures
        self.draw_image(c, faculty_signature_path, metadata["signatures"]["faculty_coordinator"])
        self.draw_image(c, principal_signature_path, metadata["signatures"]["principal"])

        # Cleanup QR
        if os.path.exists(qr_path):
            os.remove(qr_path)

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer
