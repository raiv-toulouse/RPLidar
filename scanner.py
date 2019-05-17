from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import QThread, pyqtSignal
from rplidar import RPLidar
import numpy as np
import logging,time

class Lidar(QThread):
    # Signal pour envoyer les scans
    newScansReceived = pyqtSignal(np.ndarray,np.ndarray,np.ndarray,np.ndarray)

    def __init__(self):
        super().__init__()
        self.lidar = RPLidar('COM12',baudrate=256000)
        #self.lidar = RPLidar('/dev/ttyUSB0', baudrate=256000)
        #self.connect()
        print('connexion avec le lidar')
        self.lidar.logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        #self.lidar.logger.addHandler(consoleHandler)
        info = self.lidar.get_info()
        print(info)
        health = self.lidar.get_health()
        print(health)
        print("####################")
        time.sleep(2)
        self.continuer = True

    def run(self):
        gen = self.lidar.scan2ArrayFromLidar(45,135,225,315)
        while self.continuer:
            radiusRight, thetaRight, radiusLeft, thetaLeft = next(gen)
            self.newScansReceived.emit(radiusRight,thetaRight,radiusLeft,thetaLeft)
        print("fin du thread Lidar")
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

########################################################################################################################
class MyWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.zoneDeTexte = QListWidget()
        self.mainLayout.addWidget(self.zoneDeTexte)
        self.graphe = pg.PlotWidget()
        self.mainLayout.addWidget(self.graphe)
        btn = QPushButton("Stop")
        btn.clicked.connect(self.stopScan)
        self.mainLayout.addWidget(btn)
        self.lidarThread = Lidar()
        self.lidarThread.start()
        self.lidarThread.newScansReceived.connect(self.afficherScans)
        self.plotItem = self.graphe.getPlotItem()
        self.plotDataItemLeft = self.plotItem.plot([], pen=None,symbolBrush=(255, 0, 0), symbolSize=5, symbolPen=None)
        self.plotDataItemRight = self.plotItem.plot([], pen=None,symbolBrush=(0, 255, 0), symbolSize=5, symbolPen=None)
        self.i = 0

    def setData(self, radius, theta,plotDataItem):
        print(self.i)
        self.i += 1
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        #plotDataItem.setData(x, y)

    def afficherScans(self,radiusRight,thetaRight,radiusLeft,thetaLeft):
        self.setData(radiusRight,np.deg2rad(thetaRight),self.plotDataItemRight)
        self.setData(radiusLeft,np.deg2rad(thetaLeft),self.plotDataItemLeft)
        # for angle, distance in np.nditer([thetaRight,radiusRight]):
        #     self.zoneDeTexte.addItem("angle = {}, dist = {}".format(angle, distance))
        # for angle, distance in np.nditer([thetaLeft,radiusLeft]):
        #     self.zoneDeTexte.addItem("{} , angle = {}, dist = {}".format(angle, distance))

    def stopScan(self):
        print("On arrête")
        self.lidarThread.continuer = False

########################################################################################################################
def main():
    app = QApplication([])
    pg.setConfigOptions(antialias=False) # True seems to work as well
    win = MyWidget()
    win.show()
    win.resize(800,600)
    win.raise_()
    app.exec_()

if __name__ == "__main__":
    main()