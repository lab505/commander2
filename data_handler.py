# coding:utf-8
import json
import img_utils

class DataHandler():
    def __init__(self, rc):
        self.rc = rc

    def process_received_video(self, data):
        str_img = data['data']
        pil_img = img_utils.str_to_img(str_img)
        self.rc.main_window.show_realtime_quickview(data)
        '''
        self.rc.quickview_store.add_a_quickview(
            pil_img,
            sensor_type=data.get('sensor_type', 'unknown'),
            aircraft_type=data.get('aircraft_type', 'unknown'),
        )
        '''

        print ('[data handler]recv an img from a video')

    def process_received_quickview(self, data):
        str_img = data['data']
        pil_img = img_utils.str_to_img(str_img)
        self.rc.main_window.show_realtime_quickview(data)
        '''
        self.rc.quickview_store.add_a_quickview(
            pil_img,
            sensor_type=data.get('sensor_type', 'unknown'),
            aircraft_type=data.get('aircraft_type', 'unknown'),
        )
        '''

        print('[data handler]recv an img')

    def process_received_data(self, data):
        data = json.loads(data)
        if data['type'] == 'str':
            print ('[data handler]recv a str: %s' % data['data'])
        elif data['type'] == 'quickview':
            self.process_received_quickview(data)
        elif data['type'] == 'video':
            self.process_received_video(data)
        else:
            print ('[data handler]unknown type: %s' % data['type'])
            return 'unknown type'
        return '0'
