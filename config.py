import os

current_dir = os.path.dirname(os.path.abspath(__file__))

config = {
    'data_server_ip': '127.0.0.1',
    'data_server_port': '9998',
    'quickview_filter_item_preload': {
        'aircraft_type': [],
        'sensor_type': [],
    },
}

def get_config():
    return config
