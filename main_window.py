# coding:utf-8
import os, sys, logging, functools, threading, time
import mysql.connector
import load_libs
import PyQt5
import resource_context
import quickview_monitor
import gis_canvas
import mission_widget
import fly_mission_widget
import start_logo_form
import login_dialog
import mid_term_experiment

class Commonder_Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        self.init_resource()

        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)
        self.init_widgets()
        self.init_actions()
        self.init_language()
        self.fix_screen_resolution(percentage=0.95)
        self.gis_canvas.zoom_to_sihuan()

    def fix_screen_resolution(self, percentage=0.9):
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*percentage, screenRect.height()*percentage)

    def init_widgets(self):
        self.init_quickview_monitors_widgets()
        self.init_quickview_monitors_view(2, 2)
        self.init_gis_canvas()
        self.init_fly_mission_widget()
        self.init_mission_widget()
        # self.init_logo_label()
        self.init_view()
        self.init_actions()

    def init_actions(self):
        self.show_history_quickviews.triggered.connect(self.show_history_quickviews_func)
        self.debug.triggered.connect(self.debug_button_click)
        self.zoom_to_china.triggered.connect(self.gis_canvas.zoom_to_china)
        self.use_chinese.triggered.connect(self.init_language)
        self.show_quickview.triggered.connect(self.refresh_widgets_visible)
        self.show_mission.triggered.connect(self.refresh_widgets_visible)
        self.show_map.triggered.connect(self.refresh_widgets_visible)
        self.actioncreate_area.triggered.connect(self.rc.mission_widget.show_add_area_dialog)
        self.actionmid_term.triggered.connect(functools.partial(mid_term_experiment.create_mid_term_experiment, self.rc))
        self.actiongenerate_files.triggered.connect(functools.partial(mid_term_experiment.generate_files, self.rc))
        self.actionopen_route_files.triggered.connect(functools.partial(mid_term_experiment.show_wpt_routes, self.rc))

        self.actionshow_1_quickviews.triggered.connect(functools.partial(self.init_quickview_monitors_view, 1, 1))
        self.actionshow_2_quickviews_h.triggered.connect(functools.partial(self.init_quickview_monitors_view, 2, 1))
        self.actionshow_2_quickviews_v.triggered.connect(functools.partial(self.init_quickview_monitors_view, 1, 2))
        self.actionshow_4_quickviews.triggered.connect(functools.partial(self.init_quickview_monitors_view, 2, 2))

        self.actionuse_open_street_map.triggered.connect(functools.partial(self.gis_canvas.load_online_map, 'openstreetmap'))
        self.actionuse_open_street_map_cycle.triggered.connect(functools.partial(self.gis_canvas.load_online_map, 'openstreetmap_cycle'))
        self.actionuse_amap_6.triggered.connect(functools.partial(self.gis_canvas.load_online_map, 'amap6'))
        self.actionuse_amap_7.triggered.connect(functools.partial(self.gis_canvas.load_online_map, 'amap7'))

        self.actionuse_epsg4326.triggered.connect(functools.partial(self.gis_canvas.set_projection, 'EPSG:4326'))
        self.actionuse_epsg3857.triggered.connect(functools.partial(self.gis_canvas.set_projection, 'EPSG:3857'))
    
    def init_view(self):
        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.main_vertical_layout = PyQt5.QtWidgets.QHBoxLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.left_widget = PyQt5.QtWidgets.QWidget(self)
        self.left_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.left_widget.setLayout(self.left_layout)
        self.setCentralWidget(self.main_widget)
        self.refresh_widgets_visible()

    def init_logo_label(self):
        self.logolabel = PyQt5.QtWidgets.QLabel(self)
        img = PyQt5.QtGui.QPixmap('logo.png')
        print('size:', img.size())
        img = img.scaledToWidth(400)
        print('size:', img.size())
        self.logolabel.setPixmap(img)

    def refresh_widgets_visible(self):
        #self.left_layout.addWidget(self.logolabel , 1)
        self.left_layout.addWidget(self.mission_widget, 5)
        self.main_vertical_layout.addWidget(self.left_widget, 1)
        self.main_vertical_layout.addWidget(self.gis_canvas, 2)
        self.main_vertical_layout.addWidget(self.quickview_widget, 2)
        self.main_layout.addLayout(self.main_vertical_layout, 5)
        self.main_layout.addWidget(self.fly_mission_widget, 1)
        for x in range(self.quickview_layout.maxcols):
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[y][x].clear_img()

        if self.show_quickview.isChecked():
            self.quickview_widget.show()
        else:
            self.quickview_widget.hide()
        if self.show_mission.isChecked():
            self.left_widget.show()
        else:
            self.left_widget.hide()
        if self.show_map.isChecked():
            self.gis_canvas.show()
        else:
            self.gis_canvas.hide()
        
        self.fly_mission_widget.show()
    
    def init_language(self):
        if self.use_chinese.isChecked():
            self.setWindowTitle('指挥车任务规划系统')

            self.mainmenu_mission.setTitle('任务')
            self.actioncreate_area.setText('添加飞行区域')

            self.mainmenu_view.setTitle('视图')
            self.show_quickview.setText('显示快视图')
            self.show_map.setText('显示地图')
            self.show_mission.setText('显示任务视图')
            self.use_chinese.setText('use chinese')

            self.mainmenu_map.setTitle('地图控件')
            self.zoom_to_china.setText('缩放至中国')
            
            self.actionuse_open_street_map.setText('使用Open street map')
            self.actionuse_open_street_map_cycle.setText('使用Open street map cycle')
            self.actionuse_amap_6.setText('使用高德卫星(有偏)')
            self.actionuse_amap_7.setText('使用高德地图(有偏)')
 

            self.mainmenu_quickview.setTitle('快视图')
            self.show_history_quickviews.setText('显示历史快视图')
            self.actionshow_1_quickviews.setText('显示1张快视图')
            self.actionshow_2_quickviews_h.setText('水平显示2张快视图')
            self.actionshow_2_quickviews_v.setText('垂直显示2张快视图')
            self.actionshow_4_quickviews.setText('显示4张快视图')

            self.mainmenu_help.setTitle('帮助')
        else:
            self.setWindowTitle('commander')
            self.mainmenu_mission.setTitle('mission')
            self.mainmenu_view.setTitle('view')
            self.show_quickview.setText('show quickview')
            self.show_map.setText('show map')
            self.show_mission.setText('show mission')
            self.use_chinese.setText('中文')

            self.actioncreate_area.setText('create area')

            self.mainmenu_map.setTitle('map')
            self.zoom_to_china.setText('zoom to china')
            
            self.actionuse_open_street_map.setText('use Open street map')
            self.actionuse_open_street_map_cycle.setText('use Open street map cycle')
            self.actionuse_amap_6.setText('use amap 6')
            self.actionuse_amap_7.setText('use amap 7')

            self.mainmenu_quickview.setTitle('quickview')
            self.show_history_quickviews.setText('show history quickviews')
            self.actionshow_1_quickviews.setText('show 1 quickviews')
            self.actionshow_2_quickviews_h.setText('show 2 quickviews horizontal')
            self.actionshow_2_quickviews_v.setText('show 2 quickviews vertical')
            self.actionshow_4_quickviews.setText('show 4 quickviews')

            self.mainmenu_help.setTitle('help')

    def debug_button_click(self):
        self.gis_canvas.setParent(None)
        self.gis_canvas.showMaximized()
        self.gis_canvas.show()

    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)
    
    def init_mission_widget(self):
        self.mission_widget = mission_widget.Mission_Widget(self, self.rc)

    def init_gis_canvas(self):
        self.gis_canvas = gis_canvas.Gis_Canvas(self, self.rc)

    def init_fly_mission_widget(self):
        self.fly_mission_widget = fly_mission_widget.Fly_Mission_Widget(self, self.rc)
    
    def init_quickview_monitors_widgets(self):
        self.quickview_widget = PyQt5.QtWidgets.QWidget(self)
        self.quickview_layout = PyQt5.QtWidgets.QGridLayout(self)
        self.quickview_widget.setLayout(self.quickview_layout)
        self.quickview_layout.maxrows = 2
        self.quickview_layout.maxcols = 2
        self.quickview_monitors = {}
        self.quickview_monitors_mat = []

        def init_one_quickview_monitor(x, y):
            name = '%d_%d' % (x, y)
            one_monitor = quickview_monitor.Quickview_Monitor(self, self.rc, name)
            self.quickview_monitors[name] = one_monitor
            self.quickview_layout.addWidget(one_monitor, x, y)
            return one_monitor
        for x in range(self.quickview_layout.maxcols):
            self.quickview_monitors_mat.append([])
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[x].append(init_one_quickview_monitor(x, y))

    def init_quickview_monitors_view(self, rows, cols):
        for x in range(self.quickview_layout.maxcols):
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[y][x].clear_img()
                if x < cols and y < rows:
                    self.quickview_monitors_mat[y][x].show()
                else:
                    self.quickview_monitors_mat[y][x].hide()

    def show_realtime_quickview(self, quickview_data):
        for one_monitor in self.quickview_monitors.values():
            one_monitor.check_and_show_quickview(quickview_data)
            

    def show_history_quickviews_func(self):
        quickviews = self.rc.quickview_store.get_all_quickviews()
        for quickview in quickviews:
            img = quickview['img_pil']
            img.show()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    
    SHOW_LOGO = ('-show_logo' in sys.argv)
    NEED_LOGIN = ('-login' in sys.argv)

    if SHOW_LOGO:
        start_logo_form = start_logo_form.Start_LOGO_Form()
        start_logo_form.show()
    
    def show_mainwindow():
        main_window_form = Commonder_Main()
        main_window_form.show()
    
    if NEED_LOGIN:
        login_dialog = login_dialog.Login_Dialog(show_mainwindow)
        login_dialog.show()
    else:
        show_mainwindow()
    if SHOW_LOGO:
        def close_start_logo_form():
            time.sleep(3)
            start_logo_form.close()
        threading.Thread(target = close_start_logo_form, daemon=True).start()
    sys.exit(app.exec_())
