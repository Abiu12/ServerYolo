import cv2
from ultralytics import YOLO
from yolo.utils.draw_utils import draw_boxes
from yolo.utils.file_utils import return_image


def process_image(file_path):
    img = cv2.imread(file_path)
    model = YOLO('best200.pt')
    # model = YOLO('/home/app/best200.pt')
    pred = model.predict(img)[0]
    boxes = pred.boxes.cpu().numpy()
    classes_id = boxes.cls
    names = [model.names[int(element)] for element in classes_id]
    output_image = draw_boxes(img, boxes, names)
    return return_image(output_image, names)
