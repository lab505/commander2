import PyQt5.QtCore, time, threading, qgis.gui, qgis.core, math, logging
from mission_planning import route_planning

class Point_Simulation():
    def __init__(self, rc, start_position):
        self.rc = rc

        self.label = PyQt5.QtWidgets.QLabel(self.rc.gis_canvas)
        self.label.show()
        self.label.resize(50, 50)
        self.label.setText('plane')

        icon_path="pics/icon/aoxiang.png"
        self.icon=PyQt5.QtGui.QPixmap(icon_path)
        self.icon = self.icon.scaled(PyQt5.QtCore.QSize(50, 50))
        self.label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label.setPixmap(self.icon)
        self.move_label_to_geo_point(start_position[0], start_position[1])
    
    def move_label_to_geo_point(self, x, y):
        x, y = self.rc.gis_canvas.to_map_point((x, y), 'EPSG:4326')
        x, y = self.rc.gis_canvas.to_window_point(x, y)
        self.label.move(x-25, y-25)

    def to_map_qgspoint(self, geo_point):
        mapx, mapy = self.rc.gis_canvas.to_map_point(geo_point, 'EPSG:4326')
        return qgis.core.QgsPointXY(mapx, mapy)

    def move_to(self, new_position, direction_to_east):
        icon_transform=PyQt5.QtGui.QTransform()
        icon_transform.rotate(90 - direction_to_east)
        self.label.setPixmap(self.icon.transformed(icon_transform))
        self.move_label_to_geo_point(new_position[0], new_position[1])

    def hide(self):
        self.label.hide()

class Polyline_Simulation():
    def __init__(self, rc, polyline, area_name = '', mission_name = '', need_judge_if_mission_exist = True):
        self.rc = rc
        self.polyline = polyline
        self.area_name, self.mission_name = area_name, mission_name
        self.need_judge_if_mission_exist = need_judge_if_mission_exist

    def judge_if_mission_exist(self):
        if self.need_judge_if_mission_exist:
            return self.rc.mission_manager.exist_mission(self.area_name, self.mission_name)
        else:
            return True
    
    def begin(self):
        self.point_simu = Point_Simulation(self.rc, self.polyline[0])
        self.simulation_steps = self.get_simulation_steps()
        self.step_i = 0
        self.next_step()

    def next_step(self):
        if self.step_i < len(self.simulation_steps) and self.judge_if_mission_exist():
            step = self.simulation_steps[self.step_i]
            self.step_i += 1
            self.point_simu.move_to(step['point'], step['direction'])
            PyQt5.QtCore.QTimer.singleShot(int(step['sleep_s']*1000), lambda: self.next_step())
        else:
            self.point_simu.hide()
    
    def get_simulation_steps(self):
        def get_direction_to_east(p1, p2):
            delta_x = p2[0] - p1[0]
            delta_y = p2[1] - p1[1]
            direction = 90.
            if abs(delta_x) < 0.000001:
                if delta_y > 0:
                    direction = 90.
                else:
                    direction = -90
            else:
                direction = math.atan(delta_y / delta_x) / math.pi * 180.
                if delta_x < 0:
                    direction += 180.
            return direction

        step_m = 30.
        space_s = 0.1
        simulation_steps = []
        for i in range(len(self.polyline)-1):
            p_start, p_end = self.polyline[i], self.polyline[i+1]
            direction = get_direction_to_east(p_start, p_end)
            segment_length_m = route_planning.get_meters_between_2_gps_points(p_start[0], p_start[1], p_end[0], p_end[1])
            steps = int(segment_length_m // step_m)
            if steps==0:
                steps=1
            real_step_m = segment_length_m / float(steps)
            real_space_s = real_step_m / step_m * space_s
            delta_y, delta_x = p_end[1] - p_start[1], p_end[0] - p_start[0]
            for j in range(steps):
                x, y = p_start[0] + delta_x / steps * j, p_start[1] + delta_y / steps * j
                simulation_steps.append({
                    'point': (x, y),
                    'direction': direction,
                    'sleep_s': real_space_s,
                })
        return simulation_steps
    
    
    # Old thread way, crash sometimes. Can be deleted.
    # self.simulate_thread = threading.Thread(target = self.run, daemon=True)
    # self.simulate_thread.start()
    def run(self):
        try:
            for step in self.simulation_steps:
                self.point_simu.move_to(step['point'], step['direction'])
                time.sleep(step['sleep_s'])
            self.point_simu.hide()
        except Exception as e:
            logging.exception(e)