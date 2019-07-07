# coding:utf-8
import mysql_utils, img_utils
import PIL
import PIL.Image

class QuickviewStore():
    def __init__(self, rc):
        self.rc = rc
        self.mysql_conn = mysql_utils.get_a_connection()
        self.table_name = 'quick_view'
        mysql_utils.exec_no_rsp_cmd('USE commander_db', self.mysql_conn)

    def add_a_quickview(self,
                        img_pil,
                        sensor_type='unknown',
                        sensor_id='unknown',
                        aircraft_type='unknown',
                        aircraft_id='unknown',
                        monitor_type='unknown',
                        ):
        assert isinstance(img_pil, PIL.Image.Image), 'Please use pillow image'
        img_str_data = img_utils.img_to_str(img_pil).replace('\'', '\"')
        cmd = 'INSERT INTO %s ' % self.table_name
        cmd = cmd + '(img_str_data,sensor_type,sensor_id,aircraft_type,aircraft_id)'
        cmd = cmd + ' VALUES '
        cmd = cmd + "('%s','%s','%s','%s','%s')" % (img_str_data,sensor_type,sensor_id,aircraft_type,aircraft_id)
        return (mysql_utils.exec_no_rsp_cmd(cmd, self.mysql_conn))

    def delete_all_quickviews_in_db(self):
        cmd = 'DELETE FROM %s' % self.table_name
        return (mysql_utils.exec_no_rsp_cmd(cmd, self.mysql_conn))

    def get_all_quickviews(self):
        cmd = 'SELECT img_str_data,sensor_type,sensor_id,aircraft_type,aircraft_id,add_into_table_time FROM %s' % self.table_name
        res = mysql_utils.exec_rsp_cmd(cmd, self.mysql_conn)
        quickviews = []
        for i in range(len(res)):
            img_str_data,sensor_type,sensor_id,aircraft_type,aircraft_id,add_into_table_time = res[i]
            one_quickview = {
                'img_pil': img_utils.str_to_img(img_str_data),
                'sensor_type': sensor_type,
                'sensor_id': sensor_id,
                'aircraft_type': aircraft_type,
                'aircraft_id': aircraft_id,
                'add_into_table_time': add_into_table_time
            }
            quickviews.append(one_quickview)
        return quickviews

if __name__ == '__main__':
    store_ = QuickviewStore('testrc')
    img = PIL.Image.open('pics/uav_img/0.jpg')
    store_.delete_all_quickviews_in_db()
    print (store_.add_a_quickview(img))
    store_.get_all_quickviews()[0]['img_pil'].show()
    store_.get_all_quickviews()[0]['img_pil'].show()
