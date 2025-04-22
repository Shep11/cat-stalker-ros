from example_interfaces.srv import AddTwoInts

import rclpy
import time
from rclpy.node import Node
import cv2

## This class is missing the method to publish to cat_in_picture_topic based on the output of our picture scanning program
## This class is missing code to tell the robot to stop playing if a false message is received on play_with_cat_topic

#cap = cv2.VideoCapture(0)



class CatDetectorClientAsync(Node):

    def __init__(self):
        super().__init__('cat_detector_serv')
        self.cli = self.create_client(AddTwoInts, 'cat_detector')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again... ')
        self.req = AddTwoInts.Request()

    def send_request(self, angle, dis):
        self.req.a = angle
        self.req.b = dis
        return self.cli.call_async(self.req)
rclpy.init()
detact_client = CatDetectorClientAsync()

class CatPlayClientAsync(Node):

    def __init__(self):
        super().__init__('cat_play_service')
        self.cli = self.create_client(AddTwoInts, 'play_with_cat')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again... ')
        self.req = AddTwoInts.Request()

    def send_request(self, angle, dis):
        self.req.a = angle
        self.req.b = dis
        return self.cli.call_async(self.req)
play_client = CatPlayClientAsync()

class CheckCat(Node):

    def __init__(self):
        super().__init__('check_cat')
        self.srv = self.create_service(AddTwoInts, 'check_for_cat', self.check_for_cat_callback)

    def check_for_cat_callback(self, request, response):
        #ret, frame = cap.read()
        response.sum = request.a + request.b
        #cv2.imwrite("temp.jpg", frame)
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        future = detact_client.send_request(request.a, request.b)
        rclpy.spin_until_future_complete(detact_client, future)
        print(future.result)
        print(type(future.result))
        
        if future.result().sum:
            future = play_client.send_request(request.a, request.b)
            rclpy.spin_until_future_complete(play_client, future)

        return response


def main(args=None):
    
    
    
    
    
    
    check_cat = CheckCat()
    
    rclpy.spin(check_cat)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
