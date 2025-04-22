from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import os
import time


# message import type!
# use /msgs OR BOOL



"""
TODO:

listen for motion cap.
take pic.


DONE: run pic through model.
DONE: publish true/false
"""
model = tf.keras.models.load_model("cat_detector.h5") #might need to relocate

class CatDetectorNode(Node):
    def __init__(self):
        super().__init__('cat_detector_serv')
        
        self.srv = self.create_service(AddTwoInts, 'cat_detector', self.detect_cat)
        
        self.get_logger().info('Cat Detector Node started')

    def detect_cat(self, request, response):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        image_path = "temp.jpg"
        
        cv2.imwrite(image_path, frame)
        #time.sleep(5)
        cap.release()

        # Resize image
        img = image.load_img(image_path, target_size=(224, 224))  

        # convert to array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize to [0, 1]

        # RUN IMAGE THROUGH MODEL
        prediction = model.predict(img_array)

        is_cat = False

        # The lower the value, the higher the likelihood that there's a cat.
        if prediction[0][0] < 0.5:
            is_cat = True # cat found
        else:
            is_cat = False # not a cat

        self.get_logger().info(f'Cat detected in {image_path}: {is_cat}. Prediction: {prediction[0][0]}')
        
        if (is_cat):
            response.sum = 1
        else: 
            response.sum = 0
        #os.remove(image_path)
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CatDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
