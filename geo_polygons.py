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
    
    aoxiang_big= {
        'vertex': [(117.3907016689,39.56220776172),(117.3968242257,39.563983612339),(117.402340589,39.55276695),(117.3950662638,39.55131799923)],
        'geo_ref': 'EPSG:4326'
    }
    aoxiang_huge= {
        'vertex': [(117.33424588668,39.539774638),(117.428343598759,39.540268286476),(117.42994389998,39.48298168),(117.33552612766,39.483475734)],
        'geo_ref': 'EPSG:4326'
    }
    #aoxiang_huge_str = '117.39512549903627,39.55989209995738,0 117.40394404390956,39.563686641080864,0 117.41016487788994,39.55514863160168,0 117.40134633301665,39.55130091345303,0'

    #aoxiang_huge = {
        #'vertex': [(float(x), float(y)) for x, y, z in [v_.split(',') for v_ in aoxiang_huge_str.split(' ')]],
        #'geo_ref': 'EPSG:4326'
    #}

    aoxiang_fly_round = {
        'vertex': get_round((117.40326043577984, 39.556887940996866), 1500),
        'geo_ref': 'EPSG:4326'
    }