from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('templates', exist_ok=True)

width, height = 1920, 1080
template = Image.new('RGBA', (width, height), (0, 0, 0, 0))

draw = ImageDraw.Draw(template)

border_width = 40
border_color = (255, 215, 0, 200)

draw.rectangle([0, 0, width, border_width], fill=border_color)
draw.rectangle([0, height - border_width, width, height], fill=border_color)
draw.rectangle([0, 0, border_width, height], fill=border_color)
draw.rectangle([width - border_width, 0, width, height], fill=border_color)

corner_size = 100
corner_color = (255, 215, 0, 255)

draw.polygon([(0, 0), (corner_size, 0), (0, corner_size)], fill=corner_color)
draw.polygon([(width, 0), (width - corner_size, 0), (width, corner_size)], fill=corner_color)
draw.polygon([(0, height), (corner_size, height), (0, height - corner_size)], fill=corner_color)
draw.polygon([(width, height), (width - corner_size, height), (width, height - corner_size)], fill=corner_color)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
except:
    font = ImageFont.load_default()

watermark_text = "SAMPLE TEMPLATE"
text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_x = width - text_width - 60
text_y = height - text_height - 60

draw.text((text_x, text_y), watermark_text, font=font, fill=(255, 255, 255, 180))

template.save('templates/overlay_template.png', 'PNG')
print("Sample template created: templates/overlay_template.png")
print(f"Template size: {width}x{height} pixels")
print("This is a transparent PNG with a golden border frame and watermark text.")
print("\nYou can replace this with your own template image.")
