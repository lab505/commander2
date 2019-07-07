# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5

import geo_polygons


POLYGON_AS_CLOCKWISE = True

def points_to_QgsLine(points_list):
    return qgis.core.QgsGeometry.fromPolyline(
        [qgis.core.QgsPoint(x, y) for x, y in points_list]
    )


def points_to_simple_QgsPolygon(points_list):
    return qgis.core.QgsGeometry.fromPolygonXY([
        [qgis.core.QgsPointXY(x, y) for x, y in points_list]
    ])

def trans_point(source_crs, dest_crs, x, y):
    ori_p = qgis.core.QgsPoint(x, y)
    res_p = trans_geometry(source_crs, dest_crs, ori_p)
    return res_p.x(), res_p.y()

def trans_points_list(source_crs, dest_crs, points_list):
    return [trans_point(source_crs, dest_crs, x, y) for x, y in points_list]

def trans_geometry(source_crs, dest_crs, geometry):
    transform = qgis.core.QgsCoordinateTransform(
        qgis.core.QgsCoordinateReferenceSystem(source_crs),
        qgis.core.QgsCoordinateReferenceSystem(dest_crs),
        qgis.core.QgsProject.instance())
    geometry.transform(transform)
    return geometry

class Gis_Canvas(qgis.gui.QgsMapCanvas):
    def __init__(self, parent, rc=None):
        self.oriparent = parent
        super(Gis_Canvas, self).__init__(parent)
        self.rc = rc
        if self.rc is not None:
            self.rc.gis_canvas = self
        self.init_member_widgets()
        self.destinationCrsChanged.connect(lambda: self.proj_label.setText(self.get_projection()))
        self.setVisible(True)
        self.set_projection('EPSG:3857')  # 设置显示投影(4326:wgs84经纬坐标直接投影)
        self.base_map_layers = []
        self.mission_layers = []
        self.on_draw_polygon = False
        self.load_online_map('amap6')
        self.zoom_to_aoxiang()
        self.setParallelRenderingEnabled(True)
        self.setCachingEnabled(True)
        self.refresh()

    def fullscreen(self):
        self.oriparent = self.parentWidget()
        self.setParent(None)
        self.showFullScreen()

    def exit_fullscreen(self):
        self.setParent(self.oriparent)
        self.showNormal()
        if 'rc' in dir(self):
            if 'main_window' in dir(self.rc):
                self.rc.main_window.refresh_widgets_visible()

    def init_member_widgets(self):
        self.mouse_location_label = PyQt5.QtWidgets.QLabel(self)
        self.mouse_location_label.move(0, 0)
        self.mouse_location_label.resize(500, 20)
        self.proj_label = PyQt5.QtWidgets.QLabel(self)
        self.proj_label.move(500, 0)
        self.proj_label.resize(100, 20)
        self.proj_label.setText(self.get_projection())
        self.roam_check_box = PyQt5.QtWidgets.QCheckBox(self)
        self.roam_check_box.move(600, 0)
        self.roam_check_box.setText('漫游')
        self.roam_check_box.set_checked = lambda checked: self.roam_check_box.setCheckState(PyQt5.QtCore.Qt.Checked) if checked else self.roam_check_box.setCheckState(PyQt5.QtCore.Qt.Unchecked)
        self.roam_check_box.set_checked(True)

    def show_test_label(self):
        move_x=100
        move_y=100
        angle=90
        testlabel = PyQt5.QtWidgets.QLabel(self)
        icon_path="pics/icon/aoxiang.png"
        testlabel.move(move_x, move_y)
        icon=PyQt5.QtGui.QPixmap(icon_path)
        icon =icon.scaled(PyQt5.QtCore.QSize(50, 50))
        icon_transform=PyQt5.QtGui.QTransform()
        icon_transform.rotate(angle)
        testlabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        testlabel.setPixmap(icon.transformed(icon_transform))
        testlabel.show()

    def to_window_point(self, x, y):
        center=self.getCoordinateTransform().toMapCoordinates(self.center().x(),self.center().y())
        point_window_x=self.center().x()+(x-center.x())/self.mapUnitsPerPixel()
        point_window_y=self.center().y()-(y-center.y())/self.mapUnitsPerPixel()
        return (point_window_x, point_window_y)
    
    def start_draw_polygon(self, handler_func):
        self.on_draw_polygon = True
        self.handler_func = handler_func
        self.reset_drawing_polygon()
        self.roam_check_box.set_checked(False)
    
    def reset_drawing_polygon(self):
        self.on_draw_polygon_points=[]
        if 'poly' in dir(self):
            self.poly.hide()
            del(self.poly)
        self.poly = qgis.gui.QgsRubberBand(self)
    
    def add_draw_polygon_point(self, new_point_map_location):
        assert self.on_draw_polygon
        self.on_draw_polygon_points.append(
            (new_point_map_location.x(), new_point_map_location.y()))
    
    def on_draw_polygon_mouse_move(self, new_mouse_location):
        assert self.on_draw_polygon
        if len(self.on_draw_polygon_points) > 0:
            self.poly.hide()
            del(self.poly)
            poly_to_show = self.on_draw_polygon_points + \
                [(new_mouse_location.x(), new_mouse_location.y())] + \
                self.on_draw_polygon_points[:1]
            self.poly = self.show_temp_polyline_from_points_list(poly_to_show, self.get_projection(), width=2)
            self.refresh()
    
    def finish_draw_a_polygon(self):
        if len(self.on_draw_polygon_points) > 3:
            transfer_points_list=self.clockwise_on_draw_points(self.on_draw_polygon_points)
            if not POLYGON_AS_CLOCKWISE:
                transfer_points_list.reverse()
            self.handler_func(transfer_points_list, self.get_projection())
        self.reset_drawing_polygon()

    def stop_draw_polygon(self):
        self.on_draw_polygon = False
        self.reset_drawing_polygon()
        self.roam_check_box.set_checked(True)

    def show_right_click_menu(self, pos):
        menu = PyQt5.QtWidgets.QMenu(self)
        if self.isFullScreen():
            menu.addAction('退出全屏显示').triggered.connect(self.exit_fullscreen)
        else:
            menu.addAction('全屏显示').triggered.connect(self.fullscreen)
        
        menu.addSeparator()
        menu.addAction('使用web墨卡托投影(epsg3857)').triggered.connect(lambda: self.set_projection('EPSG:3857'))
        menu.addAction('使用wgs84经纬度投影(epsg4326)').triggered.connect(lambda: self.set_projection('EPSG:4326'))
        menu.addSeparator()
        menu.addAction('使用 open street map(较快)').triggered.connect(lambda: self.load_online_map('openstreetmap'))
        menu.addAction('使用 google 卫星图(快)').triggered.connect(lambda: self.load_online_map('google_sate'))
        menu.addAction('使用 open street map cycle(较快)').triggered.connect(lambda: self.load_online_map('openstreetmap_cycle'))
        menu.addAction('使用 google 带路网的卫星图(路网有偏,慢)').triggered.connect(lambda: self.load_online_map('google_sate_with_road'))
        menu.addAction('使用高德地图(有偏,快)').triggered.connect(lambda: self.load_online_map('amap7'))
        menu.addAction('使用高德卫星图(有偏,快)').triggered.connect(lambda: self.load_online_map('amap6'))
        menu.move(pos)
        menu.show()

    def mousePressEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            self.press_location = mouse_map_location = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
            if self.on_draw_polygon:
                self.add_draw_polygon_point(mouse_map_location)
        elif event.buttons() == PyQt5.QtCore.Qt.RightButton:
            if self.on_draw_polygon:
                self.reset_drawing_polygon()
            else:
                self.show_right_click_menu(event.globalPos())

        super(Gis_Canvas, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.on_draw_polygon==True:
            self.finish_draw_a_polygon()
        super(Gis_Canvas, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        mouse_map_coordinates = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())

        mouse_map_x, mouse_map_y = mouse_map_coordinates.x(), mouse_map_coordinates.y()
        mouse_lon, mouse_lat = trans_point(self.get_projection(), 'EPSG:4326', mouse_map_x, mouse_map_y)
        self.mouse_location_label.setText('x: %.3f        y: %.3f        lon: %.3f        lat: %.3f' % (
            mouse_map_x, mouse_map_y, mouse_lon, mouse_lat))

        if self.on_draw_polygon:
            self.on_draw_polygon_mouse_move(mouse_map_coordinates)

        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            if self.roam_check_box.isChecked() and 'press_location' in dir(self):
                self.setCenter(qgis.core.QgsPointXY(
                    self.center().x() - mouse_map_coordinates.x() + self.press_location.x(),
                    self.center().y() - mouse_map_coordinates.y() + self.press_location.y()))
                self.refresh()

        super(Gis_Canvas, self).mouseMoveEvent(event)

    '''
    加载在线WMS地图
    '''
    def load_online_map(self, source):
        new_base_map_layer = None
        if source == 'openstreetmap':
            url = 'a.tile.openstreetmap.org/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db'
            service_uri = "type=xyz&zmin=0&zmax=19&url=http://" + url
            new_base_map_layer = qgis.core.QgsRasterLayer(service_uri, 'base_map', 'wms')
        elif source == 'openstreetmap_cycle':
            url = 'tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db'
            service_uri = "type=xyz&zmin=0&zmax=19&url=http://" + url
            new_base_map_layer = qgis.core.QgsRasterLayer(service_uri, 'base_map', 'wms')
        elif source == 'amap6':
            service_uri = "type=xyz&url=http://webst04.is.autonavi.com/appmaptile?style%3D6%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=18&zmin=0"
            new_base_map_layer = qgis.core.QgsRasterLayer(service_uri, 'base_map', 'wms')
        elif source == 'amap7':
            service_uri = "type=xyz&url=http://webst04.is.autonavi.com/appmaptile?style%3D7%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=18&zmin=0"
            new_base_map_layer = qgis.core.QgsRasterLayer(service_uri, 'base_map', 'wms')
        elif source == 'google_sate':
            new_base_map_layer = qgis.core.QgsRasterLayer(
                'type=xyz&url=http://www.google.com/maps/vt?lyrs%3Ds@189%26gl%3Dus%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=21&zmin=0',
                'base_map', 'wms')
        elif source == 'google_sate_with_road':
            new_base_map_layer = qgis.core.QgsRasterLayer(
                'type=xyz&url=http://www.google.com/maps/vt?lyrs%3Dy@189%26gl%3Dus%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=21&zmin=0',
                'base_map', 'wms')
        elif source == 'ESRI_Imagery_World_2D':
            new_base_map_layer = qgis.core.QgsRasterLayer("http://server.arcgisonline.com/arcgis/rest/services/ESRI_Imagery_World_2D/MapServer?f=json&pretty=true","raster")
        else:
            raise 'unknown online map source %s' % str(source)
        for old_base_map_layer in self.base_map_layers:
            qgis.core.QgsProject.instance().removeMapLayer(old_base_map_layer)
        self.base_map_layers = [new_base_map_layer]
        qgis.core.QgsProject.instance().addMapLayer(new_base_map_layer, True)
        self.setLayers(self.mission_layers + self.base_map_layers)
        self.refresh()

    '''
    设置显示投影
    '''
    def set_projection(self, epsg_code):
        self.setDestinationCrs(qgis.core.QgsCoordinateReferenceSystem(epsg_code))
        self.refresh()
    
    def get_projection(self):
        return self.mapSettings().destinationCrs().authid()

    def test_load_shapefile(self):
        import platform
        sys_name = platform.system().lower()
        shapefile_name = ''
        if sys_name.startswith('darwin'):  # mac
            shapefile_name = '/Applications/QGIS3.app/Contents/Resources/resources/data/world_map.shp'
        elif sys_name.startswith('win'):  # windows
            shapefile_name = 'C:/Program Files/QGIS 3.6/apps/qgis/resources/data/world_map.shp'
        else:
            raise 'unknown system'
        shapefile_layer = qgis.core.QgsVectorLayer(shapefile_name, 'world_map_from_shapefile', 'ogr')
        qgis.core.QgsProject.instance().addMapLayer(shapefile_layer, True)
        self.mission_layers = [shapefile_layer] + self.mission_layers
        self.setLayers(self.mission_layers + self.base_map_layers)
        self.refresh()

    def show_temp_polyline_from_points_list( \
            self,
            points_list,
            epsgcode,
            color=PyQt5.QtCore.Qt.black,
            width=10,
            line_style=PyQt5.QtCore.Qt.SolidLine, #DashLine, DotLine, DashDotLine, DashDotDotLine
                ):
        poly = qgis.gui.QgsRubberBand(self, qgis.core.QgsWkbTypes.LineGeometry)
        geom = points_to_QgsLine(points_list)
        geom = trans_geometry(epsgcode, self.get_projection(), geom)
        poly.setToGeometry(geom, None)
        poly.setColor(color)
        poly.setWidth(width)
        poly.setLineStyle(line_style)
        poly.show()
        return poly
    
    def to_map_point(self, point, epsgcode):
        map_epsgcode = self.get_projection()
        x, y = point
        return trans_point(epsgcode, map_epsgcode, x, y)

    def show_temp_points_from_points_list(self, points_list, epsgcode, width=1, color=PyQt5.QtCore.Qt.black):
        poly = qgis.gui.QgsRubberBand(self, qgis.core.QgsWkbTypes.PointGeometry)
        for x, y in points_list:
            x, y = self.to_map_point((x, y), epsgcode)
            poly.addPoint(qgis.core.QgsPointXY(x, y))
        poly.setColor(color)
        poly.setWidth(width)
        poly.show()
        return poly

    def show_temp_polygon_from_points_list(self, points_list, epsgcode, width=1, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.yellow):
        poly = qgis.gui.QgsRubberBand(self)
        geom = points_to_simple_QgsPolygon(points_list)
        geom = trans_geometry(epsgcode, self.get_projection(), geom)
        poly.setToGeometry(geom, None)
        poly.setColor(edgecolor)
        poly.setFillColor(fillcolor)
        poly.setWidth(width)
        poly.show()
        return poly

    def add_polygon_layer_from_points_list(self, points_list, epsgcode):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:%s&field=fldtxt:string" % epsgcode, "layer", "memory")
        f = qgis.core.QgsFeature()
        g = points_to_simple_QgsPolygon(points_list)
        f.setGeometry(g)
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def add_polygon_layer_from_wkt(self, wkt_str, epsgcode):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:%s&field=fldtxt:string" % epsgcode, "layer", "memory")
        f = qgis.core.QgsFeature()
        geo = qgis.core.QgsGeometry.fromWkt(wkt_str)
        f.setGeometry(geo)
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def test_add_geometry(self):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=fldtxt:string", "layer", "memory")
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(15, 31, 18, 33)))
        layer.dataProvider().addFeatures([f])
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(30, 20, 50, 80)))
        layer.dataProvider().addFeatures([f])
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(156.71, 50.93, 156.72, 50.94)))
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def zoom_to_rectangle(self, min_x, min_y, max_x, max_y, epsg_code):
        map_epsg_code = self.get_projection()
        min_x_map, min_y_map = trans_point(epsg_code, map_epsg_code, min_x, min_y)
        max_x_map, max_y_map = trans_point(epsg_code, map_epsg_code, max_x, max_y)
        self.setExtent(qgis.core.QgsRectangle(min_x_map, min_y_map, max_x_map, max_y_map))
        self.refresh()
    
    def zoom_to_polygon(self, vertex, epsg_code):
        minx = maxx = vertex[0][0]
        miny = maxy = vertex[0][1]
        for x, y in vertex:
            minx = min(minx, x)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
            miny = min(miny, y)
        centerx = (minx+maxx)/2.
        centery = (miny+maxy)/2.
        minx = minx*2-centerx
        maxx = maxx*2-centerx
        miny = miny*2-centery
        maxy = maxy*2-centery
        self.zoom_to_rectangle(minx, miny, maxx, maxy, epsg_code)

    def zoom_to_china(self):
        self.zoom_to_rectangle(74, 10, 135, 54, 'EPSG:4326')

    def zoom_to_pku(self):
        self.zoom_to_rectangle(116.294, 39.980, 116.315, 40, 'EPSG:4326')

    def zoom_to_sihuan(self):
        self.zoom_to_rectangle(116.280, 39.85, 116.46, 39.97, 'EPSG:4326')
    
    def zoom_to_aoxiang(self):
        self.zoom_to_polygon(geo_polygons.Polygons.aoxiang['vertex'], geo_polygons.Polygons.aoxiang['geo_ref'])

    def clockwise_on_draw_points(self,points):
        n=0
        x_min_value=points[0][0]
        y_value=points[0][1]
        length=len(points)
        for i in range(length):
            if points[i][0]<x_min_value:
                n=i
                x_min_value=points[i][0]
            elif points[i][0]==x_min_value:
                if points[i][1]>y_value:
                    n = i
                    x_min_value = points[i][0]
                    y_value=points[i][1]
        #作差积，判断多边形为顺时针还是逆时针
        x1=points[n][1]-points[(n-1+length)%length][0]
        y1=points[n][1]-points[(n-1+length)%length][1]
        x2 = points[(n + 1) % length][0] - points[n][0]
        y2 = points[(n + 1) % length][1] - points[n][1]
        vector=x1*y2-x2*y1
        points_list=[]
        for point in points:
            points_list.append((point[0],point[1]))
        if(vector>0):
            points_list.reverse()
        return points_list


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.fix_screen_resolution()

        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.canvas = Gis_Canvas(self)
        self.main_layout.addWidget(self.canvas)
        self.drawed_polygon = []
        self.drawed_polygon_rubber_band = []


        #设置button布局
        self.hbox = PyQt5.QtWidgets.QHBoxLayout()
        self.gridGroupBox= PyQt5.QtWidgets.QGroupBox('')
        self.button_layout = PyQt5.QtWidgets.QGridLayout()
        self.button_layout.setSpacing(5)
        self.gridGroupBox.setLayout(self.button_layout)
        self.hbox.addWidget(self.gridGroupBox)

        import functools

        self.to_china_button = PyQt5.QtWidgets.QPushButton('移动到中国',self)
        self.button_layout.addWidget(self.to_china_button,0,0)
        self.to_china_button.clicked.connect(self.to_china_click)

        self.start_draw_button=PyQt5.QtWidgets.QPushButton('开始绘制多边形',self)
        self.button_layout.addWidget(self.start_draw_button,0,1)
        self.start_draw_button.clicked.connect(self.start_draw_click)

        self.stop_draw_button = PyQt5.QtWidgets.QPushButton('结束绘制多边形', self)
        self.button_layout.addWidget(self.stop_draw_button,0,2)
        self.stop_draw_button.clicked.connect(self.stop_draw_click)

        self.clean_current_button = PyQt5.QtWidgets.QPushButton('删除当前多边形', self)
        self.button_layout.addWidget(self.clean_current_button, 0, 3)
        self.clean_current_button.clicked.connect(self.clean_current_click)

        self.clean_all_button = PyQt5.QtWidgets.QPushButton('删除所有多边形', self)
        self.button_layout.addWidget(self.clean_all_button, 0, 4)
        self.clean_all_button.clicked.connect(self.clean_all_click)

        b = PyQt5.QtWidgets.QPushButton('use_amap', self)
        self.button_layout.addWidget(b, 0, 5)
        b.clicked.connect(functools.partial(
            self.canvas.load_online_map, 'amap6'))

        b = PyQt5.QtWidgets.QPushButton('use_openstreetmap', self)
        self.button_layout.addWidget(b, 0, 6)
        b.clicked.connect(functools.partial(
            self.canvas.load_online_map, 'openstreetmap'))

        b = PyQt5.QtWidgets.QPushButton('zoom to aoxiang', self)
        self.button_layout.addWidget(b, 0, 7)
        b.clicked.connect(lambda: self.canvas.zoom_to_polygon(geo_polygons.Polygons.aoxiang['vertex'], geo_polygons.Polygons.aoxiang['geo_ref']))

        b = PyQt5.QtWidgets.QPushButton('set_epsg4326', self)
        self.button_layout.addWidget(b, 0, 8)
        b.clicked.connect(functools.partial(
            self.canvas.set_projection, 'EPSG:4326'))

        b = PyQt5.QtWidgets.QPushButton('fullscreen', self)
        self.button_layout.addWidget(b, 0, 9)
        b.clicked.connect(self.canvas.fullscreen)

        b = PyQt5.QtWidgets.QPushButton('exit fullscreen', self)
        self.button_layout.addWidget(b, 0, 10)
        b.clicked.connect(self.canvas.exit_fullscreen)

        b = PyQt5.QtWidgets.QPushButton('show test label', self)
        self.button_layout.addWidget(b, 0, 11)
        b.clicked.connect(self.canvas.show_test_label)

        self.main_layout.addLayout(self.hbox)

    
    def fix_screen_resolution(self, percentage=0.9):
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*percentage, screenRect.height()*percentage)

    def to_china_click(self):
        self.canvas.zoom_to_china()

    def draw_polygon_handler_func(self, one_polygon, epsgcode):
        self.drawed_polygon.append([one_polygon])
        self.drawed_polygon_rubber_band.append(
            self.canvas.show_temp_polygon_from_points_list(one_polygon, epsgcode))
        self.canvas.show_temp_points_from_points_list(one_polygon, width=100, epsgcode=epsgcode)

    def start_draw_click(self):
        self.canvas.start_draw_polygon(self.draw_polygon_handler_func)

    def stop_draw_click(self):
        self.canvas.stop_draw_polygon()

    def clean_current_click(self):
        if len(self.drawed_polygon):
            self.drawed_polygon_rubber_band[-1].hide()
            del(self.drawed_polygon[-1])
            del(self.drawed_polygon_rubber_band[-1])

    def clean_all_click(self):
        for i in range(len(self.drawed_polygon)):
            self.drawed_polygon_rubber_band[-1].hide()
            del(self.drawed_polygon[-1])
            del(self.drawed_polygon_rubber_band[-1])

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
