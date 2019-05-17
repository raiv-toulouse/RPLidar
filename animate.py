#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM12'
DMAX = 4000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    print(num)
    scan = next(iterator)
    print(scan)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME,baudrate=256000)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    try:
        iterator = lidar.scanAllDataFromLidar() #lidar.iter_scans()
        ani = animation.FuncAnimation(fig, update_line,
            fargs=(iterator, line), interval=100)
        plt.show()
    finally:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    run()
