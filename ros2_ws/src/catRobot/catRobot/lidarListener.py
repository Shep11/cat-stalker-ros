from sweeppy import Sweep

import sys
import rclpy
from rclpy.node import Node
import math

from example_interfaces.srv import AddTwoInts


print("hello")

conv = 57295.779513082
value = 30

class PositionClientAsync(Node):

    def __init__(self):
        super().__init__('cat_pos_service')
        self.cli = self.create_client(AddTwoInts, 'position')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again... ')
        self.req = AddTwoInts.Request()

    def send_request(self, angle, dis):
        self.req.a = angle
        self.req.b = dis
        return self.cli.call_async(self.req)


def blowup(samp, old, b):
    x = samp.distance * math.cos(samp.angle * conv)
    y = samp.distance * math.sin(samp.angle * conv)
    x1 = old[b - 1].distance * math.cos(old[b-1].angle * conv)
    y1 = old[b - 1].distance * math.sin(old[b-1].angle * conv)

    x2 = old[b].distance * math.cos(old[b].angle * conv)
    y2 = old[b].distance * math.sin(old[b].angle * conv)

    x11 = 0
    xx = x - x1
    yy = y - y1
    y11 = 0
    y21 = y2 - y1
    x21 = x2 - x1

    v1d = ((yy)**2 + (xx)**2)**(1/2)
    v1t = math.atan(yy/xx)

    v2d = ((y21)**2 + (x21)**2)**(1/2)
    v2t = math.atan(y21/x21)
    
    proj = math.sin(v1t - v2t) * v1d

    if (proj > value):
        print(proj)
        return True
    return False


def main():
    rclpy.init()

    #pos_client = PositionClientAsync()


    
    with Sweep('/dev/ttyUSB0') as sweep:
        sweep.start_scanning()
        
        old = next(sweep.get_scans()).samples
        global out
        while True:
            scan = sweep.get_scans()
            out = None
            d = 0
            b = 0
            temp = next(scan).samples
            for samp in temp:
                while (b < len(old) - 1 and old[b].angle < samp.angle):
                    b = b + 1

                if (samp.distance > 10 and samp.distance < 100):
                    if(blowup(samp, old, b)):
                        out = samp
                        d = d + 1
                    else:
                        d = 0
                        out = None
                    if d > 25:
                        break
                else:
                    (temp.remove(samp))
                    
            old = temp
            print(out)







if __name__ == '__main__':
    main()
