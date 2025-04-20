import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty
import time

# TODO: EVERYTHING

class ImageCaptureNode(Node):
    def __init__(self):

        super().__init__('image_capture_node')
        
        self.subscription = self.create_subscription(
            Empty, 'motion_detected', self.capture_image, 10)

        self.publisher_ = self.create_publisher(String, 'image_captured', 10)

        self.camera = "?"

        self.image_dir = '/tmp/cat_images'
        # create directory?

        self.get_logger().info('Image Capture Node started')

    def capture_image(self, msg):
        timestamp = int(time.time())
        image_path = f'{self.image_dir}/image_{timestamp}.jpg'

        # camera.takePic

        # take picture
        # save to image_path

        self.get_logger().info(f'Image captured: {image_path}')
        msg = String()
        msg.data = image_path
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImageCaptureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
