from example_interfaces.srv import AddTwoInts

import rclpy
import time
from rclpy.node import Node
import cv2

## This class is missing the method to publish to cat_in_picture_topic based on the output of our picture scanning program
## This class is missing code to tell the robot to stop playing if a false message is received on play_with_cat_topic

cap = cv2.VideoCapture(0)

class CheckCat(Node):

    def __init__(self):
        super().__init__('check_cat')
        self.srv = self.create_service(AddTwoInts, 'check_for_cat', self.check_for_cat_callback)

    def check_for_cat_callback(self, request, response):
        ret, frame = cap.read()
        response.sum = request.a + request.b
        cv2.imwrite("temp.jpg", frame)
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response


def main(args=None):
    rclpy.init(args=args)
    
    check_cat = CheckCat()
    
    rclpy.spin(check_cat)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
