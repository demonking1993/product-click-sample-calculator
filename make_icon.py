from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
image = Image.new("RGBA", (SIZE, SIZE), "#17233C")
draw = ImageDraw.Draw(image)

draw.rounded_rectangle((96, 96, 928, 928), radius=192, fill="#5B5CE2")
draw.rounded_rectangle((204, 204, 820, 820), radius=136, fill="#FFFFFF")

font_paths = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
]
font = None
for path in font_paths:
    try:
        font = ImageFont.truetype(path, 432)
        break
    except OSError:
        pass
if font is None:
    font = ImageFont.load_default()

text = "款"
bbox = draw.textbbox((0, 0), text, font=font)
x = (SIZE - (bbox[2] - bbox[0])) / 2 - bbox[0]
y = (SIZE - (bbox[3] - bbox[1])) / 2 - bbox[1] - 16
draw.text((x, y), text, font=font, fill="#5B5CE2")

image.save("app.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
image.save("app_1024.png")
