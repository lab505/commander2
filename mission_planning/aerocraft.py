# coding=utf8
'''
class Aerocraft():
    def __init__(self,
                 type_=None,
                 max_speed_meter_per_second=None, min_speed_meter_per_second=None, normal_speed_meter_per_second=None,
                 max_height_meter=None, min_height_meter=None, normal_height_meter=None,
                 max_distance_meter=None, residual_energy_percent=1,
                 ):
        self.type = type_  # 飞行器类型
        self.max_speed_meter_per_second=max_speed_meter_per_second  # 最大航速/(m/s)
        self.min_speed_meter_per_second=min_speed_meter_per_second  # 最小航速/(m/s)
        self.normal_speed_meter_per_second=normal_speed_meter_per_second  # 正常航速/(m/s)
        self.max_height_meter=max_height_meter  # 最大航高/m
        self.min_height_meter=min_height_meter  # 最小航高/m
        self.normal_speed_meter_per_second=normal_height_meter  # 正常航高/m
        self.max_distance_meter=max_distance_meter  # 最大航程/m
        self.residual_energy_percent=residual_energy_percent  # 剩余能量百分比
'''
aerocrafts = {
    '猛牛-轻小型固定翼无人机(演示短航程)': {
        'name': '猛牛-轻小型固定翼无人机(演示短航程)',
        'max_v_km_h': 115.2,
        'suggest_v_km_h': 100.8,
        'min_v_km_h': 64.8,
        'max_height_m': 1000,
        'min_height_m': 100,
        'max_mileage_km': 20,
    },
    '翱翔号': {
        'name': '翱翔号',
        'max_v_km_h': 126.0,
        'suggest_v_km_h': 100.,
        'min_v_km_h': 72.0,
        'max_height_m': 300,
        'min_height_m': 100,
        'max_mileage_km': 140,
    },
    '猛牛-轻小型固定翼无人机': {
        'name': '猛牛-轻小型固定翼无人机',
        'max_v_km_h': 115.2,
        'suggest_v_km_h': 100.8,
        'min_v_km_h': 64.8,
        'max_height_m': 300,
        'min_height_m': 100,
        'max_mileage_km': 150,
    },
    '猛牛-轻小型固定翼无人机(搭载sar)': {
        'name': '猛牛-轻小型固定翼无人机(搭载sar)',
        'max_v_km_h': 115.2,
        'suggest_v_km_h': 100.8,
        'min_v_km_h': 64.8,
        'max_height_m': 1000,
        'min_height_m': 100,
        'max_mileage_km': 150,
    },
    '海豚-轻小型固定翼无人机': {
        'name': '海豚-轻小型固定翼无人机',
        'max_v_km_h': 108,
        'suggest_v_km_h': 97.2,
        'min_v_km_h': 100.8,
        'max_height_m': 300,
        'min_height_m': 100,
        'max_mileage_km': 97.2,
    },
    '滑翔机-轻小型固定翼无人机': {
        'name': '滑翔机-轻小型固定翼无人机',
        'max_v_km_h': 90,
        'suggest_v_km_h': 64.8,
        'min_v_km_h': 72,
        'max_height_m': 300,
        'min_height_m': 50,
        'max_mileage_km': 150,
    },
    '长航时固定翼无人机': {
        'name': '长航时固定翼无人机',
        'max_v_km_h': 230,
        'suggest_v_km_h': 170,
        'min_v_km_h': 150,
        'max_height_m': 7500,
        'min_height_m': 200,
        'max_mileage_km': 2040,
    },
    '多旋翼无人机': {
        'name': '多旋翼无人机',
        'max_v_km_h': 40,
        'suggest_v_km_h': 10,
        'min_v_km_h': 0,
        'max_height_m': 1000,
        'min_height_m': 0,
        'max_mileage_km': 5,
    },
    '飞艇': {
        'name': '多旋翼无人机',
        'max_v_km_h': 80,
        'suggest_v_km_h': 35,
        'min_v_km_h': 0,
        'max_height_m': 2000,
        'min_height_m': 0,
        'max_mileage_km': 105,
    },
    '系留气球': {
        'name': '多旋翼无人机',
        'max_v_km_h': 0,
        'suggest_v_km_h': 0,
        'min_v_km_h': 0,
        'max_height_m': 1000,
        'min_height_m': 100,
        'max_mileage_km': 0,
        #因为定点工作所以速度是0
    }
}