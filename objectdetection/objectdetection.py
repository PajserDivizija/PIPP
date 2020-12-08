#python3.8.5
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
from random import randint
import sys


def color_generator():
    color = []
    for i in range(3):
        color.append(randint(0,255)-randint(0,255)%10)
    return tuple(color)

def get_people_coordinates(image_path):
    #'coco.names', 'yolo3.weights', 'yolov3.cfg' must exist in cwd
    
    try:
        f = open("coco.names")
        f = open("yolov3.weights")
        f = open("yolov3.cfg")
    except IOError:
        print('File from CWD missing')
        exit()
    classes = None

    image = plt.imread(image_path)
    height, width, ch = image.shape
    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # read pre-trained model and config file
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    net.setInput(cv2.dnn.blobFromImage(image, 1/255.0, (416,416), (0,0,0), True, crop=False))
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)


    boxes = []
    class_ids = []
    confidences = []
    boxes = []
    #puts results in different lists (linked by order)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    #finds the best-fitting box
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)


    # im = Image.open(image_path) #opening input picture for drawing
    # draw_im = ImageDraw.Draw(im)

    correct_boxes = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        if class_ids[i]==0:
            x,y,w,h = box
            correct_boxes.append([x,y,x+w,y+h])
            # draw_im.rectangle([x,y,x+w,y+h],outline=color_generator(),width=3)
    
    # im.show()
    
    return correct_boxes