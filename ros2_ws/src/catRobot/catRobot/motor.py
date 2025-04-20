
import lgpio
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

# The idea behind this code is, recieve the bool message frm play_with_cat_topic. 
# If this is a True message, spin the motors forward for 5 seconds, and spin the motor reverse for 5 seconds

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
          # Turn the motor forward at 10% speed for 5 seconds
          lgpio.tx_pwm(h, FORWARD, FREQ, 10)
          time.sleep(5)
          # Turn the motor reverse at 10% speed for 10 seconds
          lgpio.tx_pwm(h, REVERSE, FREQ, 10)
          time.sleep(5)
          
    
except KeyboardInterrupt:
    # Stop sending power to both pins
    lgpio.tx_pwm(h, FORWARD, FREQ, 0)
    lgpio.tx_pwm(h, REVERSE, FREQ, 0)
    lgpio.gpiochip_close(h)


