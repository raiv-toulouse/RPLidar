from rplidar import RPLidar
import numpy as np
import logging,time

print('debut')
lidar = RPLidar('COM12',baudrate=256000)

#lidar = RPLidar('/dev/ttyUSB0', baudrate=256000)
print('connexion')

lidar.logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
#lidar.logger.addHandler(consoleHandler)

try:
    info = lidar.get_info()
    print(info)

    health = lidar.get_health()
    print(health)

    print("####################")
    time.sleep(2)

    gen = lidar.scan2DataFromLidar(45,135,225,315)
    i=0
    while True:
        scanRight, scanLeft = next(gen)
        i+=1
        print('===========================  %d: Got %d measures from right scan' % (i, len(scanRight)))
        for (quality, angle, distance) in scanRight:
            print(quality, angle, distance)
        print('===========================  %d: Got %d measures from right scan' % (i, len(scanLeft)))
        for (quality, angle, distance) in scanLeft:
            print(quality, angle, distance)
        if i > 2:
            break
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

