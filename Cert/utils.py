from PIL import Image, ImageDraw, ImageFont

def generate_certificate(template_path, output_path, name, usn):
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)

    # Example positioning
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((200, 200), name, fill="black", font=font)
    draw.text((200, 300), usn, fill="black", font=font)

    img.save(output_path)