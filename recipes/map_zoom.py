#Skrypt ten ma na celu umzliwienie nam przyblizenie mapy do danej skali na podane wspolrzedne punktu
#w okreslonymm ukladzie wspolrzednych.
#Jacek Dankiewicz

##x=string
##y=string
##skala=number 1000
##EPSG=number 2180

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#definiowanie ukladu wspolrzednych oraz wspolrzednych punktu
ct = iface.mapCanvas().mapRenderer().destinationCrs()
cf = QgsCoordinateReferenceSystem()
cf.createFromId(EPSG)                                             
crsTransform = QgsCoordinateTransform(cf, ct)
wspolrzedne = QgsPoint(float(x), float(y))
geom = QgsGeometry.fromPoint(wspolrzedne)                                      
geom.transform(crsTransform)                                             

#okreslanie skali przyblizenia
s=skala
center = geom.asPoint()
rect = QgsRectangle(center, center)                                      
iface.mapCanvas().setExtent(rect)                                   
iface.mapCanvas().zoomScale(s)                          
iface.mapCanvas().refresh() 

#ustalanie rodzaju, koloru i rozmiaru znaku
m = QgsVertexMarker(iface.mapCanvas())
m.setIconType(QgsVertexMarker.ICON_CROSS)
m.setColor(QColor(255,0,0))
m.setCenter(geom.asPoint())
m.setIconSize(6)
m.setPenWidth(3)

#ustawianie czasu po jakim znak zniknie
def timer_fired():
    iface.mapCanvas().scene().removeItem(m)
    timer.stop()

timer = QTimer()
timer.timeout.connect(timer_fired)
timer.setSingleShot(True)
timer.start(2000)
