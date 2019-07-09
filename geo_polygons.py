from mission_planning import route_planning
import math

class Rectangles:
    pku = {
        'min': (116.294, 39.980),
        'max': (116.315, 40.),
        'geo_ref': 'EPSG:4326'
    }
    china = {
        'min': (74., 10.),
        'max': (135., 54.),
        'geo_ref': 'EPSG:4326'
    }

def get_round(center, radius_m):
    get_coor_trans_mat = route_planning.get_coor_trans_mat
    one_point_coor_trans = route_planning.one_point_coor_trans

    delta_ = 0.001
    poly_ = [
        (center[0] - delta_, center[1] - delta_),
        (center[0] + delta_, center[1] - delta_),
        (center[0] + delta_, center[1] + delta_),
        (center[0] - delta_, center[1] + delta_),
    ]
    trans_mat, inv_trans_mat = get_coor_trans_mat(poly_, '4326', (1, 0))
    center_trans = one_point_coor_trans(center[0], center[1], trans_mat)
    vertex_num = 20
    round_points = []
    for i in range(vertex_num+1):
        deg_ = float(i) / vertex_num * math.pi * 2
        x = center_trans[0] + radius_m * math.cos(deg_)
        y = center_trans[1] + radius_m * math.sin(deg_)
        x, y = one_point_coor_trans(x, y, inv_trans_mat)
        round_points.append((x, y))
    return round_points


class Polygons:
    pku = {
        'vertex': [
            (116.294, 39.980),
            (116.294, 40.),
            (116.315, 40.),
            (116.315, 39.980),
            ],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang = {
        'vertex': [(117.39913559,39.561335192),(117.40438137646,39.563165225661),(117.41021328,39.5550088),(117.4048795794,39.55292997333)],
        'geo_ref': 'EPSG:4326'
    }
    
    aoxiang_big_str = '117.395555,39.5618444,0 117.4057396,39.566206,0 117.416328,39.55137,0 117.406548,39.5465758,0'

    aoxiang_big = {
        'vertex': [(float(x), float(y)) for x, y, z in [v_.split(',') for v_ in aoxiang_big_str.split(' ')]],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang_huge_str = '117.39514872977733,39.55994251511356,0 117.40440145098901,39.56313256315074,0 117.41007328633593,39.55506375273477,0 117.40069461547252,39.551590097197646,0'

    aoxiang_huge = {
        'vertex': [(float(x), float(y)) for x, y, z in [v_.split(',') for v_ in aoxiang_huge_str.split(' ')]],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang_fly_round = {
        'vertex': get_round((117.40244325956651, 39.557765433008804), 5000),
        'geo_ref': 'EPSG:4326'
    }