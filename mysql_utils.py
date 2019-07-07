# coding:utf-8

import unittest, logging, warnings, time, sys, platform
import mysql.connector
import base64

sys_name = platform.system().lower()

def get_a_connection():
    option_files = 'my.ini'
    if sys_name.startswith('darwin'):
        option_files = 'my.ini.mac'
    warnings.simplefilter("ignore", ResourceWarning)
    return mysql.connector.connect(option_files=option_files)

def exec_rsp_cmd(cmd_, conn_):
    try:
        mycursor = conn_.cursor()  # 使用cursor()方法获取操作游标
        mycursor.execute(cmd_)
        res_batch = []
        for x in mycursor:
            res_batch.append(x)
        mycursor.close()
        conn_.commit()
        return res_batch
    except Exception as e:
        logging.exception(e)
        return []

def exec_no_rsp_cmd(cmd_, conn_):
    try:
        mycursor = conn_.cursor()
        mycursor.execute(cmd_)
        conn_.commit()
        mycursor.close()
        return True
    except Exception as e:
        logging.exception(e)
        return False

def show_dbs(conn_):
    res = []
    tup_batch = exec_rsp_cmd('SHOW DATABASES', conn_)
    for tup in tup_batch:
        res.extend(tup)
    return res

def create_db(name_, conn_):
    return exec_no_rsp_cmd('CREATE DATABASE %s' % name_, conn_)

def create_db_if_not_exist_and_select_it(name_, conn_):
    if name_ not in show_dbs(conn_):
        create_db(name_, conn_)
    exec_no_rsp_cmd('USE %s' % name_, conn_)

def drop_db(name_, conn_):
    return exec_no_rsp_cmd('DROP DATABASE %s' % name_, conn_)

def create_table_if_not_exists(name_, fields_, conn_):
    if name_ not in show_tables(conn_):
        create_table(name_, fields_, conn_)

def create_table(name_, fields_, conn_):
    return exec_no_rsp_cmd('CREATE TABLE IF NOT EXISTS %s %s' % (name_, fields_), conn_)

def drop_table(name_, conn_):
    return exec_no_rsp_cmd('DROP TABLE %s' % (name_), conn_)

def drop_table_if_exists(name_, conn_):
    if name_ in show_tables(conn_):
        drop_table(name_, conn_)

def desc_table(name_, conn_):
    return exec_rsp_cmd('DESC %s' % (name_), conn_)

def show_tables(conn_):
    res = []
    for table in exec_rsp_cmd('SHOW TABLES', conn_):
        res.extend(table)
    return res


class Mysql_Handler(object):
    def __init__(self, option_files='C:\\mysql-8.0.15-winx64\\mysql-8.0.15-winx64\\my.ini', db_name='mission_planning_db', table_name='mission_planning_table'):
        self._db_name, self._table_name = db_name, table_name
        self._conn = get_a_connection(option_files=option_files)
        create_db_if_not_exist_and_select_it(self._db_name, self._conn)
        create_table_if_not_exists(self._table_name, '(name VARCHAR(100), val VARCHAR(20000), UNIQUE KEY unique_name(name))', self._conn)

    def erase(self, k):
        cmd = "DELETE FROM %s WHERE name='%s'" % (self._table_name, k)
        return exec_no_rsp_cmd(cmd, self._conn)

    def push(self, k, v):
        self.erase(k)
        cmd = "INSERT INTO %s VALUES ('%s', '%s')" % (self._table_name, k, v)
        exec_no_rsp_cmd(cmd, self._conn)
        self._conn.commit()

    def get(self, k):
        cmd = "SELECT val FROM %s WHERE name = '%s'" % (self._table_name, k)
        res = exec_rsp_cmd(cmd, self._conn)
        if len(res) > 0:
            return res[0][0]
        else:
            return None

    def select_all(self):
        cmd = "SELECT * FROM %s" % (self._table_name)
        res = exec_rsp_cmd(cmd, self._conn)
        return res

class _UnitTest(unittest.TestCase):
    def test_get_a_connection(self):
        conn_ = get_a_connection()
        print (conn_)
        print (show_dbs(conn_))

if __name__ == '__main__':
    unittest.main()
