import pyqtgraph as pg

plot = pg.plot()
plot.setAspectLocked()

# Add polar grid lines
plot.addLine(x=0, pen=0.2)
plot.addLine(y=0, pen=0.2)
for r in range(2, 20, 2):
    circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r*2, r*2)
    circle.setPen(pg.mkPen(0.2))
    plot.addItem(circle)

# make polar data
import numpy as np
theta = np.linspace(0, 2*np.pi, 100)
radius = np.random.normal(loc=10, size=100)

# Transform to cartesian and plot
x = radius * np.cos(theta)
y = radius * np.sin(theta)
plot.plot(x, y)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
