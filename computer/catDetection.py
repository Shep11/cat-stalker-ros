import rclpy
from rclpy.node import Node
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np



from cat-stalker.msg import CatFound

# message import type!
# use /msgs OR BOOL


"""
TODO:

listen for motion cap.
take pic.


DONE: run pic through model.
DONE: publish true/false
"""

class CatDetectorNode(Node):
    def __init__(self):
        super().__init__('cat_detector_node')

        # subscribe to image capture. TEMPORARY
        self.subscription = self.create_subscription(
            String, 'image_captured', self.detect_cat, 10)
        
        self.publisher_ = self.create_publisher(CatFound, 'cat_detected', 10)

        self.model = tf.keras.models.load_model("cat_model/cat_detector.h5") #might need to relocate

        self.get_logger().info('Cat Detector Node started')

    def detect_cat(self, msg):
        image_path = msg.data

        # Resize image
        img = image.load_img(imgage_path, target_size=(224, 224))  

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

        out_msg = CatFound()
        out_msg.is_cat = is_cat
        out_msg.image_path = image_path
        self.publisher_.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = CatDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()