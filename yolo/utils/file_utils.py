import os
import time
import cv2
from PIL import Image
from io import BytesIO
import base64


def save_file(file, folder):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.filename)
    file.save(file_path)
    return file_path


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def return_image(image, names):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # output_path = os.path.join('outputs', f"image_{timestamp}.jpg")
    # # output_path = f"outputs/{}"
    # cv2.imwrite(output_path, image)
    # Convert image to base64
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # remove_file(output_path)
    return {
        "image_name": f"image_{timestamp}.jpg",
        "names": names,
        "image_base64": img_base64
    }
