# import mysql.connector
#from flask import current_app
import sqlite3
import os

def get_connection():
    # 获取当前文件所在目录
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # # 计算数据库文件的相对路径，回到上一级目录找到数据库文件
    # db_path = os.path.join(base_dir, '..', 'sky31Employees.db')
    conn = sqlite3.connect('sky31Employees.db')
    return conn