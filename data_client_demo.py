# coding:utf-8
import sys, socket, config, json, os, time, random, threading, cv2, img_utils
import numpy as np
from PIL import Image, ImageDraw, ImageFont

cfg = config.get_config()


def split_data(data_, part_length=4096):
    while len(data_) > 0:
        send, data_ = data_[:part_length], data_[part_length:]
        yield send


def send_data_to_ip_port(ip, port, data_):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        data_ = data_.encode('utf8')
        for part in split_data(data_):
            sock.sendall(part)
            response = str(sock.recv(1024), 'utf8')
        sock.sendall('end'.encode('utf8'))
        response = str(sock.recv(1024), 'utf8')
        return response

def send_string(ip, port, message):
    data_ = json.dumps({'type': 'str', 'data': message})
    send_data_to_ip_port(ip, port, data_)
    print ('send string success')
    return 0

def send_img(ip, port, pil_img, aircraft_type, sensor_type,monitor_type):
    data_ = json.dumps({
        'type': 'quickview',
        'data': img_utils.img_to_str(pil_img),
        'aircraft_type': aircraft_type,
        'sensor_type': sensor_type,
        'monitor_type': monitor_type
    })
    send_data_to_ip_port(ip, port, data_)
    print ('send img success')

def get_test_image_names(dir_):
    names_ = os.listdir(dir_)
    for i in range(len(names_)):
        names_[i] = dir_ + '/' + names_[i]
    return names_

def get_test_image_names_with_sensorname(dir_):
    res = []
    dirs_ = os.listdir(dir_)
    for subdir_ in dirs_:
        abs_subdir_ = dir_ + '/' + subdir_
        names_ = os.listdir(abs_subdir_)
        for i in range(len(names_)):
            sensor_type_ = subdir_
            name_ = dir_ + '/' + subdir_ + '/' + names_[i]
            res.append((name_, sensor_type_))
    import random
    random.shuffle(res)
    return res

def normalization(img_pil):
    from PIL import Image
    import numpy as np
    img_np = np.array(img_pil)
    min_ = np.min(img_np)
    max_ = np.max(img_np)
    img_np = np.array((img_np-min_)/max_*255, dtype=np.uint8)
    img_new = Image.fromarray(img_np)
    return img_new

def is_color_img(img_pil):
    import numpy as np
    img_np = np.array(img_pil)
    if len(img_np) == 3:
        return True
    else:
        return False

def quickview_send(ip, port, folder,aircraft_type,sensor_type):
    while True:
        test_img_names=get_test_image_names(folder)
        for name_ in test_img_names:
            monitor_type='quickview'
            img = Image.open(name_)
            img = normalization(img)
            is_color_img(img)
            img = img.resize((200,200))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("songti.TTF",8)
            text_ = 'aircrafttype: %s\nsensor_type: %s' % (aircraft_type, sensor_type)
            text_color = (255, 0, 0)
            if not is_color_img(img):
                text_color = 255
            draw.text((00, 00), text_, fill = text_color, font=font)
            send_img(ip, port, img, aircraft_type, sensor_type,monitor_type)
            time.sleep(2)

def picproduct_send(ip, port, folder,aircraft_type,sensor_type):
    while True:
        test_img_names=get_test_image_names(folder)
        for name_ in test_img_names:
            monitor_type='picproduct'
            img = Image.open(name_)
            img = normalization(img)
            is_color_img(img)
            img = img.resize((1000,500))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("songti.TTF",8)
            text_ = 'aircrafttype: %s\nsensor_type: %s' % (aircraft_type, sensor_type)
            text_color = (255, 0, 0)
            if not is_color_img(img):
                text_color = 255
            draw.text((00, 00), text_, fill = text_color, font=font)
            send_img(ip, port, img, aircraft_type, sensor_type,monitor_type)
            time.sleep(2)

def video_send(ip, port,folder,aircraft_type,sensor_type):
    while True:
        files = get_test_image_names(folder)
        for file in files:
            cap = cv2.VideoCapture(file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            ret, img = cap.read()
            while (ret):
                monitor_type = 'video'
                img = normalization(img)
                is_color_img(img)
                img = img.resize((100, 100))
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("songti.TTF", 8)
                text_ = '%s\n%s' % (aircraft_type, sensor_type)
                text_color = (255, 0, 0)
                if not is_color_img(img):
                    text_color = 255
                draw.text((00, 00), text_, fill=text_color, font=font)
                send_img(ip, port, img, aircraft_type, sensor_type, monitor_type)
                ret, img = cap.read()
                # time.sleep(fps)


def main():
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    #quickview_send(ip, port, 'pics/realdata/多光谱', 'aircraft_type1', 'sensor_typea')
    #video_send(ip, port, 'pics/realdata/双波段视频吊舱_可见光', 'aircraft_type1', 'sensor_typea')
    threads = []
    
    t1 = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/光学相机影像', '北航猛牛', '光学相机影像',))
    threads.append(t1)
    #t2 = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/minisar', '北航猛牛', 'minisar',))
    #threads.append(t2)
    t3 = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/多光谱', '固定翼', '多光谱',))
    threads.append(t3)
    #t4 = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/测绘相机快视图', '猛牛', '测绘相机快视图',))
    #threads.append(t4)
    t5 = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/高光谱', '猛牛', '高光谱',))
    threads.append(t5)
    t6 = threading.Thread(target=video_send, args=(ip, port, 'pics/realdata/双波段视频吊舱_可见光', '地理所xxx', '双波段视频吊舱_可见光',))
    threads.append(t6)
    t7 = threading.Thread(target=video_send, args=(ip, port, 'pics/realdata/双波段视频吊舱_红外', '北航猛牛2', '双波段视频吊舱_红外',))
    threads.append(t7)
    t8 = threading.Thread(target=video_send, args=(ip, port, 'pics/realdata/光学相机视频', '北航猛牛2', '光学相机视频',))
    threads.append(t8)
    
    #t9 = threading.Thread(target=picproduct_send, args=(ip, port, 'pics/realdata/快视遥感产品/', '猛牛', '测绘相机快视图',))
    #threads.append(t9)#快视产品显示
    
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()



if __name__ == '__main__':
    main()
