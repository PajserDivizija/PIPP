from paz.applications import HaarCascadeFrontalFace, MiniXceptionFER
import paz.processors as pr
import cv2
import numpy as np
from paz.backend.image import load_image, show_image

class EmotionDetector(pr.Processor):
    def __init__(self):
        super(EmotionDetector, self).__init__()
        self.detect = HaarCascadeFrontalFace(draw=False)
        self.crop = pr.CropBoxes2D()
        self.classify = MiniXceptionFER()
        self.draw = pr.DrawBoxes2D(self.classify.class_names)

    def call(self, image):
        boxes2D = self.detect(image)['boxes2D']
        cropped_images = self.crop(image, boxes2D)
        for cropped_image, box2D in zip(cropped_images, boxes2D):
            box2D.class_name = self.classify(cropped_image)['class_name']
        return self.draw(image, boxes2D)


detect = EmotionDetector()
# you can now apply it to an image (numpy array)
images = load_image('neo.png')
predictions = detect(images)
show_image(predictions)
