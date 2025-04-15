import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

class CatMonitor(Node):

    def __init__(self):
        super().__init__('cat_monitor')
        
        # Subscribe to cat_in_picture_topic
        self.subscription = self.create_subscription(
            Bool,
            'cat_in_picture_topic',
            self.cat_status_callback,
            10)
            
        # Publisher for play_with_cat_topic
        self.publisher = self.create_publisher(
            Bool,
            'play_with_cat_topic',
            10)
            
        # Store the latest cat status
        self.cat_in_picture = False  # Default to False to avoid unnecessary play at startup
        
        # Timer that triggers every 5 minutes 
        self.timer = self.create_timer(300.0, self.timer_callback)
        
        self.get_logger().info('Cat Monitor has started')

    def cat_status_callback(self, msg):
        # Update the status when a message is received
        self.cat_in_picture = msg.data
        self.get_logger().info(f'Received cat status: {self.cat_in_picture}')

    def timer_callback(self):
        # Check if the cat is in the picture (based on status)
        if self.cat_in_picture:
            # If cat is in picture, publish True to play_with_cat_topic
            play_msg = Bool()
            play_msg.data = True
            self.publisher.publish(play_msg)
            self.get_logger().info('Playing with cat')
        else:
            # If cat is not in picture, publish False to play_with_cat_topic
            play_msg = Bool()
            play_msg.data = False
            self.publisher.publish(play_msg)
            self.get_logger().info('Cat is not in picture, no need to play')

def main(args=None):
    rclpy.init(args=args)
    
    cat_monitor = CatMonitor()
    
    rclpy.spin(cat_monitor)
    
    cat_monitor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
