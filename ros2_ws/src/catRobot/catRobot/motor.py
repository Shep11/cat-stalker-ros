
import lgpio
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

# Configuration
FORWARD = 18 # Pin. RYAN CHANGE THIS
REVERSE = 19 # Pin. RYAN CHANGE THIS
FREQ = 10000

h = lgpio.gpiochip_open(0)

class MotorControl(Node):

    def __init__(self):
        super().__init__('motor_control')
        
        # Subscribe to play_with_cat_topic
        self.subscription = self.create_subscription(
            Bool,
            'play_with_cat_topic',
            self.playing_status_callback,
            10)
        
        self.get_logger().info('Motor control has started')   

try:
    def playing_status_callback(self, msg):
        # Update the status when a message is received
        self.playing_with_cat = msg.data
        self.get_logger().info(f'Received cat status: {self.playing_with_cat}')
        while self.playing_with_cat:
          # Turn the prismatic joint to 10% speed for 5 seconds
          lgpio.tx_pwm(h, FORWARD, FREQ, 10)
          time.sleep(5)
          # Turn the continuos joing to 10% speed for 10 seconds
          lgpio.tx_pwm(h, REVERSE, FREQ, 10)
          time.sleep(5)
          
    
except KeyboardInterrupt:
    # Turn the continous joint off
    lgpio.tx_pwm(h, CONTINUOS, FREQ, 0)
     # Turn the prismatic joint off
    lgpio.tx_pwm(h, PRISMATIC, FREQ, 0)
    lgpio.gpiochip_close(h)


