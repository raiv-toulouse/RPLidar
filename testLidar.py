from rplidar import RPLidar
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

    gen = lidar.scan2ArrayFromLidar(45, 135, 225, 315)
    i=0
    while True:
        radiusRight, thetaRight, radiusLeft, thetaLeft = next(gen)
        print(i)
        i+=1

    # for i, scan in enumerate(lidar.scanAllDataFromLidar()):
    #     print('===========================  %d: Got %d measures' % (i, len(scan)))
    #     for (quality, angle, distance) in scan:
    #         print(quality, angle, distance)
    #     if i > 2:
    #         break
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
