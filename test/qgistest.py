import os, sys, logging, platform
sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import load_libs
import gis_canvas

sys_name = platform.system().lower()

import qgis, qgis.core, PyQt5
from qgis.gui import *
#from qgis.PyQt.QtCore import SIGNAL, Qt, QString
from qgis.PyQt.QtWidgets import QMainWindow, QAction
from qgis.core import *

class MyWnd2(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1000, 1000)
        self.canvas = gis_canvas.Gis_Canvas(self)
        self.canvas.resize(500, 500)
        self.canvas.move(500, 500)
        #self.setCentralWidget(self.canvas)
        #self.toolbar = self.addToolBar("Canvas actions")


class MyWnd(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        layer = QgsVectorLayer("Polygon?crs=epsg:4326&field=fldtxt:string",
                               "layer", "memory")


        self.canvas = QgsMapCanvas()
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(15, 31, 18, 33)))
        layer.dataProvider().addFeatures([f])
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(30, 20, 50, 80)))
        layer.dataProvider().addFeatures([f])
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(156.71, 50.93, 156.72, 50.94)))
        layer.dataProvider().addFeatures([f])

        filename = ''
        if sys_name.startswith('darwin'):  # mac
            filename = '/Applications/QGIS3.app/Contents/Resources/resources/data/world_map.shp'
        elif sys_name.startswith('win'):  # windows
            filename = 'C:/Program Files/QGIS 3.6/apps/qgis/resources/data'
        else:
            raise 'unknown system'

        layer2 = QgsVectorLayer(filename, 'test', 'ogr')  # 失败

        url = 'tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db' # cycle ok
        #url = 'a.tile.openstreetmap.org/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db' # cycle ok
        service_uri = "type=xyz&zmin=0&zmax=19&url=http://" + url
        print (service_uri)
        rlayer = QgsRasterLayer(service_uri, "rlayer", "wms")
        print (layer2.crs().authid())
        print (rlayer.crs().authid())
        print (rlayer.crs().description())
        print(rlayer)
        print(rlayer.isValid())

        print ('canvas crs:' , self.canvas.mapSettings().destinationCrs().authid())
        crs=QgsCoordinateReferenceSystem('EPSG:4326')
        self.canvas.setDestinationCrs(crs)
        print ('canvas crs2:' , self.canvas.mapSettings().destinationCrs().authid())
        self.canvas.setLayers([layer, layer2, rlayer])
        print (self.canvas.layers())
        print (type(self.canvas.layers()))
        #self.canvas.setExtent(layer2.extent())
        self.canvas.setExtent(QgsRectangle(74,10,135,54))
        QgsProject.instance().addMapLayer(layer, True)
        #QgsProject.instance().addMapLayer(layer2, True)
        QgsProject.instance().addMapLayer(rlayer, True)
        self.canvas.setVisible(True)
        self.canvas.refresh()

        self.setCentralWidget(self.canvas)
        self.toolbar = self.addToolBar("Canvas actions")

logging.basicConfig(level=logging.DEBUG)
if sys_name.startswith('darwin'):  # mac
    QgsApplication.setPrefixPath("/Applications/QGIS3.app/Contents/MacOS", True)
elif sys_name.startswith('win'):  # windows
    QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.6/apps/qgis", True)
else:
    raise 'unknown system'

app = PyQt5.QtWidgets.QApplication(sys.argv)
form = MyWnd2()
form.show()
sys.exit(app.exec_())
