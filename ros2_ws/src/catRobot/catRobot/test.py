from sweeppy import Sweep

print("hello")

with Sweep('/dev/ttyUSB0') as sweep:
    sweep.start_scanning()
    
    for scan in sweep.get_scans():
        print('{}\n'.format(scan))
