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
            content = f.read()

        # Handle potential trailing data or comments in JSON files
        # Try to parse the JSON, and if it fails with "Extra data" error,
        # extract only the valid JSON portion
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            if "Extra data" in str(e):
                # Try to extract valid JSON by finding the first complete object
                try:
                    # Find the end of the first valid JSON object by tracking braces
                    brace_count = 0
                    end_pos = 0
                    in_string = False
                    escape_next = False

                    for i, char in enumerate(content):
                        if escape_next:
                            escape_next = False
                            continue

                        if char == '\\':
                            escape_next = True
                            continue

                        if char == '"' and not escape_next:
                            in_string = not in_string
                            continue

                        if not in_string:
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    # Found the end of the first JSON object
                                    end_pos = i + 1
                                    break

                    if end_pos > 0:
                        valid_json = content[:end_pos]
                        return json.loads(valid_json)
                    else:
                        raise e
                except Exception:
                    raise ValidationError(f"Invalid JSON metadata file: {self.metadata_path}")
            else:
                raise e

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

        # Calculate scaling factors between image dimensions and PDF canvas
        image_width = float(metadata["canvas"]["width"])  # 2000
        image_height = float(metadata["canvas"]["height"])  # 1414
        page_width, page_height = landscape(A4)  # (841.89, 595.28)

        scale_x = page_width / image_width
        scale_y = page_height / image_height

        # Scale image to fit
        c.drawImage(template_png, 0, 0, width=page_width, height=page_height)

        # Function to scale metadata coordinates
        def scale_meta(meta_dict):
            scaled = meta_dict.copy()
            if "x" in scaled:
                scaled["x"] *= scale_x
            if "y" in scaled:
                scaled["y"] *= scale_y
            if "width" in scaled:
                scaled["width"] *= scale_x
            if "height" in scaled:
                scaled["height"] *= scale_y
            return scaled

        # Draw text placeholders (scaled)
        placeholders = metadata["placeholders"]

        self.draw_text(c, student_name, scale_meta(placeholders["student_name"]))
        self.draw_text(c, event_name, scale_meta(placeholders["event_name"]))
        self.draw_text(c, club_name, scale_meta(placeholders["club_name"]))
        self.draw_text(c, date, scale_meta(placeholders["date"]))
        self.draw_text(c, usn, scale_meta(placeholders["usn"]))

        # AICTE points field only for AICTE template (scaled)
        if template_type == "certificate_aicte":
            self.draw_text(c, str(points), scale_meta(placeholders["points"]))

        # Generate QR Code (in-memory)
        qr_image = self.generate_qr_code(qr_text)
        qr_path = os.path.join(self.template_dir, "qr_temp.png")
        qr_image.save(qr_path)

        # Draw QR code (scaled)
        self.draw_image(c, qr_path, scale_meta(metadata["qrcode"]))

        # Draw signatures (scaled)
        self.draw_image(c, faculty_signature_path, scale_meta(metadata["signatures"]["faculty_coordinator"]))
        self.draw_image(c, principal_signature_path, scale_meta(metadata["signatures"]["principal"]))

        # Cleanup QR
        if os.path.exists(qr_path):
            os.remove(qr_path)

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer
