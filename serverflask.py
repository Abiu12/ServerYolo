from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import time
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)

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
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    return image


@app.route('/analyze', methods=['POST'])
def upload_image():
    try:
        file = request.files['image']
        file_path = os.path.join('uploads', file.filename)
        # file_path = f"/home/app/uploads/{file.filename}"
        file.save(file_path)
        img = cv2.imread(file_path)
        model = YOLO('/home/app/best200.pt')
        pred = model.predict(img)[0]
        boxes = pred.boxes.cpu().numpy()
        clases_id = boxes.cls
        names = [model.names[int(elemento)] for elemento in clases_id]
        output_image = draw_boxes(
            img, boxes, names, font_path="arial.ttf", font_size=22)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join('outputs', f"imagen_{timestamp}.jpg")
        # output_path = f"/home/app/outputs/imagen_{timestamp}.jpg"
        cv2.imwrite(output_path, output_image)
        resultados = {
            "full_path": os.path.abspath(output_path),
            "name_image": os.path.basename(output_path),
            "names": names
        }
        # Eliminar el upload
        os.remove(os.path.join('uploads', file.filename))
        # os.remove(f"/home/app/uploads/{file.filename}")
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": str(e)})


@ app.route('/delete_image/<image_name>', methods=['GET'])
def delete_image(image_name):
    try:
        os.remove(os.path.join('outputs', image_name))
        # os.remove(f"/home/app/outputs/{image_name}")
        return jsonify({"message": "Se ha eliminado correctamente la imagen."})
    except Exception as e:
        return jsonify({"error": str(e)})


@ app.route('/get_image/<image_name>')
def get_image(image_name):
    # Ruta para obtener la imagen generada por su nombre
    image_path = os.path.join('outputs', image_name)
    # image_path = f"/home/app/outputs/{image_name}"
    return send_file(image_path, mimetype='image/jpeg')


@ app.route('/testapi', methods=['GET'])
def testApi():
    return jsonify("Estamos al aire")


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    # os.makedirs('/home/app/uploads', exist_ok=True)
    # os.makedirs('/home/app/outputs', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
