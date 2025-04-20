from sweeppy import Sweep
import time

print("hello")

with Sweep('/dev/ttyUSB0') as sweep:
    sweep.start_scanning()
    
    for scan in sweep.get_scans():
        x = 0
        for s in scan.samples:
            x = x + s.distance
        print('{}\n'.format(x))
        sweep.stop_scanning()
        time.sleep(3)
        sweep.start_scanning()
