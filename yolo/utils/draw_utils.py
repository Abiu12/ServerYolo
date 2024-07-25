import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

colors = ["green", "pink", "red", "blue", "orange", "yellow"]


def draw_boxes(image, boxes, names, font_path="arial.ttf", font_size=30):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    for box, name in zip(boxes, names):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = colors[0] if name == "Araña roja" else colors[1] if name == "Mosca blanca" else colors[
            2] if name == "Alternariosis" else colors[3] if name == "Botritis" else colors[4] if name == "Mildiu del tomate" else colors[5]
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=4)
        draw.text((x1, y1 - 10), name, font=font, fill=color)
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
