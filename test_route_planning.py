# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5
import gis_canvas
import mission_planning.route_planning
import geo_polygons


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        self.fix_screen_resolution(0.9)

        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.canvas = gis_canvas.Gis_Canvas(self)
        self.main_layout.addWidget(self.canvas)

        self.button= PyQt5.QtWidgets.QPushButton(self)
        self.main_layout.addWidget(self.button)
        self.button.clicked.connect(self.onClick)

        self.canvas.zoom_to_aoxiang()

        fly_route, photo_ground_rectangles_geo, debug_info = mission_planning.route_planning.plan_a_route_for_test()
        shooting_area = debug_info['shooting_area']
        fly_route_points = [
            (fly_route_point_info['longitude'], fly_route_point_info['latitude']) for fly_route_point_info in fly_route]
        self.canvas.show_temp_points_from_points_list(
            fly_route_points, 'EPSG:4326')
        self.canvas.show_temp_polyline_from_points_list(
            fly_route_points, 'EPSG:4326',
            color=PyQt5.QtCore.Qt.blue,
            width=1,
            line_style=PyQt5.QtCore.Qt.SolidLine)
        for rec in photo_ground_rectangles_geo:
            rec_to_draw = rec+rec[:1]
            self.canvas.show_temp_polyline_from_points_list(
                rec_to_draw, 'EPSG:4326',
                color=PyQt5.QtCore.Qt.red,
                width=1,
                line_style=PyQt5.QtCore.Qt.SolidLine)

    def fix_screen_resolution(self, percentage=0.9):
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*percentage, screenRect.height()*percentage)

    def onClick(self):
        print('ok')
        self.canvas.zoom_to_china()

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
