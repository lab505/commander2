# coding:utf-8
import unittest, json
import numpy as np
import PIL
import PIL.Image

def np_to_list(input_):
    if type(input_) == np.ndarray:
        res = []
        for line_ in input_:
            res.append(np_to_list(line_))
        return res
    else:
        return int(input_)

def img_to_str(pil_img):
    res = {}
    res['mode'] = pil_img.mode
    np_format_ = np.array(pil_img)
    list_format_ = np_to_list(np_format_)
    res['data'] = list_format_
    return json.dumps(res).replace(' ', '')

def str_to_img(str_img):
    dict_like = json.loads(str_img)
    np_format_ = np.array(dict_like['data'], dtype=np.uint8)
    return PIL.Image.fromarray(np_format_, mode=dict_like['mode'])

class _UnitTest(unittest.TestCase):
    def test_np_to_list(self):
        a = [
            [[1,2],[3,4]],
            [[5,6],[8,8]],
        ]
        np_format_ = np.array(a)
        list_format_ = np_to_list(np_format_)
        print (list(np_format_))
        #print (list_format_)

    def test_img_to_str(self):
        img = PIL.Image.open('pics/uav_img/0.jpg')
        to_str = img_to_str(img)
        restr_img = str_to_img(to_str)
        print (isinstance(restr_img, PIL.Image.Image))
        restr_img.show()

if __name__ == '__main__':
    unittest.main()
