import sqlite3

# 连接到数据库
conn = sqlite3.connect('sky31Employees.db')
c = conn.cursor()

# 创建 admin 表
c.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        admin_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        pswd_hash VARCHAR(255) NOT NULL
    );
''')

# 创建 student 表
c.execute('''
    CREATE TABLE IF NOT EXISTS student (
        student_id VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        tel VARCHAR(255) NOT NULL,
        department VARCHAR(255) NOT NULL,
        role_in_depart VARCHAR(255) NOT NULL,
        pswd_hash VARCHAR(255) NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT
    );
''')

# 创建 events 表
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name VARCHAR(255) NOT NULL,
        event_date DATETIME
    );
''')

# 创建 whoLeave 表
c.execute('''
    CREATE TABLE IF NOT EXISTS whoLeave (
        whoLeave_order INTEGER PRIMARY KEY AUTOINCREMENT,
        whoLeave_id INT NOT NULL,
        whoLeave_name VARCHAR(255) NOT NULL,
        leave_reason VARCHAR(255) NOT NULL,
        check_opinion VARCHAR(255),
        is_permitted INT DEFAULT 0,
        check_time DATETIME,
        path_to_image VARCHAR(255)
    );
''')
print('会有这一步')

conn.commit()
conn.close()