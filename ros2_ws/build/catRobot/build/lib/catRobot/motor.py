
import lgpio
import time

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

#from std_msgs.msg import String
#from std_msgs.msg import Bool

# The idea behind this code is, recieve the bool message frm play_with_cat_topic. 
# If this is a True message, spin the motors forward for 5 seconds, and spin the motor reverse for 5 seconds

# Configuration
FORWARD = 17 # Pin. RYAN CHANGE THIS
REVERSE = 22 # Pin. RYAN CHANGE THIS
FREQ = 10000

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, FORWARD)
lgpio.gpio_claim_output(h, REVERSE)

class PlayWithCat(Node):

    def __init__(self):
        super().__init__('play_cat')
        self.srv = self.create_service(AddTwoInts, 'play_with_cat', self.play_callback)

    def play_callback(self, request, response):
        response.sum = request.a + request.b
        
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        
        try:
            for i in range(3):
                lgpio.gpio_write(h, REVERSE, 0)
                lgpio.gpio_write(h, FORWARD, 1)
                time.sleep(1)
                lgpio.gpio_write(h, FORWARD, 0)
                lgpio.gpio_write(h, REVERSE, 1)
            
                time.sleep(1)
        except KeyboardInterrupt:
            # Stop sending power to both pins
            lgpio.gpio_write(h, REVERSE, 0)
            lgpio.gpio_write(h, FORWARD, 0)
            lgpio.gpiochip_close(h)
        lgpio.gpio_write(h, REVERSE, 0)
        lgpio.gpio_write(h, FORWARD, 0)
        return response


def main():
    rclpy.init()
    
    play_cat = PlayWithCat()
    
    rclpy.spin(play_cat)
    
    rclpy.shutdown()
    
            

if __name__ == '__main__':
    main()
          
    



