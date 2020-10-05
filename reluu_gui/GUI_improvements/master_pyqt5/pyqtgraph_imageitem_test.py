# import initExample
from PySide2 import QtGui
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

app = QtGui.QApplication([])

## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('pyqtgraph example: ImageItem')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
# view.setAspectLocked(True)

# ## Create image item
img = pg.ImageItem(border='w')
view.addItem(img)
pos = np.array([0., 1., 0.5, 0.25, 0.75])
color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)])
cmap = pg.ColorMap(pos, color)
lut = cmap.getLookupTable(0.0, 1.0, 256)

img.setLookupTable(lut)
img.setImage(lut)
# # img.setLevels([-50,40])


# ## Set initial view bounds
view.setRange(QtCore.QRectF(0, 0, 600, 600))

# ## Create random image
data = np.random.normal(size=(15, 600, 600), loc=1024, scale=64).astype(np.uint16)
i = 0
# img.setImage(data[i])

# def updateData():
#     global img, data, i, updateTime, fps

#     ## Display the data
#     img.setImage(data[i])
#     i = (i+1) % data.shape[0]

#     QtCore.QTimer.singleShot(1, updateData)
#     now = ptime.time()
#     fps2 = 1.0 / (now-updateTime)
#     updateTime = now
#     fps = fps * 0.9 + fps2 * 0.1
    
    #print "%0.1f fps" % fps
    

# updateData()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()