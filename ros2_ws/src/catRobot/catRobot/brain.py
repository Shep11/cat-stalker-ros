import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

## This class is missing the method to publish to cat_in_picture_topic based on the output of our picture scanning program
## This class is missing code to tell the robot to stop playing if a false message is received on play_with_cat_topic

class MainFunctionality(Node):

    def __init__(self):
        super().__init__('main_fucntionality')
            
        # Publisher for cat_in_picture_topic
        self.publisher = self.create_publisher(
            Bool,
            'cat_in_picture_topic',
            10)
        
        # Subscribe to play_with_cat_topic
        self.subscription = self.create_subscription(
            Bool,
            'play_with_cat_topic',
            self.playing_status_callback,
            10)
        
        # Not playing with cat by default
        self.playing_with_cat = False 
        
        self.get_logger().info('Main Funcitonality has started')

    def playing_status_callback(self, msg):
        # Update the status when a message is received
        self.playing_with_cat = msg.data
        self.get_logger().info(f'Received cat status: {self.playing_with_cat}')


def main(args=None):
    rclpy.init(args=args)
    
    main_functionality = MainFunctionality()
    
    rclpy.spin(main_functionality)
    
    main_functionality.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
