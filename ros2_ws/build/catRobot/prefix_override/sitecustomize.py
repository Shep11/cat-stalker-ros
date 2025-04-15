import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cat/robot/cat-stalker/ros2_ws/install/catRobot'
