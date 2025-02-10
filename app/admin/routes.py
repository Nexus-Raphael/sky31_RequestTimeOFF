import sqlite3
from flask import Flask, request, session, jsonify,Blueprint
from ..models import db,Student,Admin
from ..password_utils import hashlize,check
import logging
import pandas as pd

admin_bp = Blueprint('admin', __name__)
logging.basicConfig(level=logging.INFO)


@admin_bp.route('/login', methods=['POST'])
def login():
    admin_id=request.json.get('admin_id')
    password=request.json.get('password')

    if admin_id is None or password is None:
        return jsonify({"message":"输入错误"})

    try:

        admin=Admin.query.get(int(admin_id))
        if admin is not None:
            if(check(password,admin.pswd_hash)):
                session['admin_id'] = admin.admin_id
                session['name'] = admin.name
                return jsonify({"message":"登录成功"}),200
            else:
                return jsonify({"message":"登录失败,密码错误"}),401
        else:
            return jsonify({"message":"不存在该用户"}),404

    except sqlite3.Error as e:
        return jsonify({"message": f"数据库错误：{str(e)}"}), 500


@admin_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('admin_id', None)
    session.pop('name', None)
    return jsonify({"message": "账号已退出！"}), 200

@admin_bp.route('/query', methods=['GET'])
def query_user_by_department():
    if session.get('admin_id') is None:
        return jsonify({"message": "登录状态失效！"})
    department = request.args.get('department')

    if not department:
        return jsonify({"message": "部门名称参数缺失"}), 400

    try:
        # g.cursor.execute('SELECT * FROM student WHERE department = ?', (department,))
        # users = g.cursor.fetchall()
        users=Student.query.filter_by(department=department).all()
        if not users:
            return jsonify({"message": "未找到该部门的用户"}), 404

        result = [{"id": user.id, "name": user.name, "department": user.department} for user in users]
        return jsonify({"users": result}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"数据库错误：{str(e)}"}), 500

@admin_bp.route('/idquery', methods=['GET'])
def student_idquery():
    if session.get('admin_id') is None:
        return jsonify({"message": "登录状态失效！"})
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({"message": "学号参数缺失"}), 400

    try:
        # g.cursor.execute('SELECT * FROM student WHERE student_id = ?', (student_id,))
        # users = g.cursor.fetchall()
        user=Student.query.filter(Student.student_id==student_id).first()
        if not user:
            return jsonify({"message": "未找到该用户"}), 404

        result = [{"id": user.id, "name": user.name, "department": user.department}]
        return jsonify({"users": result}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"数据库错误：{str(e)}"}), 500


@admin_bp.route('/add', methods=['POST'])
def add_user():
    student_id = request.json.get('student_id')
    name = request.json.get('name')
    department = request.json.get('department')
    role_in_depart = request.json.get('role_in_depart')
    tel = request.json.get('tel')
    password = request.json.get('password')

    try:
        password=str(password)
        pswd_hash=hashlize(password)
        pswd_hash=pswd_hash.decode('utf8')
        # g.cursor.execute('INSERT INTO student (student_id, name, tel, department, role_in_depart, password) VALUES (?,?,?,?,?,?)', (student_id, name, tel, department, role_in_depart, password))
        # g.connection.commit()
        s=Student(student_id=student_id,name=name,tel=tel,role_in_depart=role_in_depart,department=department,pswd_hash=pswd_hash)
        db.session.add(s)
        db.session.commit()
        return jsonify({"message": "用户添加成功"}), 200
    except Exception as e:
        logging.error(f"发生错误: {str(e)}")
        return jsonify({"message": f"添加用户失败: {str(e)}"}), 500


@admin_bp.route('/update', methods=['POST'])
def update_user():
    student_id = request.json.get('student_id')
    name = request.json.get('name')
    tel = request.json.get('tel')
    department = request.json.get('department')
    role_in_depart = request.json.get('role_in_depart')

    try:

        student=Student.query.filter(Student.id==student_id).update({"name":name,"tel":tel,"role_in_depart":role_in_depart,"department":department})
        db.session.commit()
        return jsonify({"message": "用户修改成功"}), 200
    except sqlite3.Error as e:
        return jsonify({"message": f"修改失败：{str(e)}"}), 500


@admin_bp.route('/delete', methods=['POST'])
def delete_user():
    student_id = request.json.get('student_id')

    try:

        student=Student.query.filter(Student.syudent_id==student_id).delete()
        db.session.commit()
        return jsonify({"message": "用户删除成功"}), 200
    except sqlite3.Error as e:
        return jsonify({"message": f"删除失败：{str(e)}"}), 500


# excel表导入
@admin_bp.route('/import', methods=['POST'])
def import_users():
    if session.get('admin_id') is None:
        return jsonify({"message": "登录状态失效！"})

    if 'file' not in request.files:
        return jsonify({"message": "未找到文件"}), 400

    file = request.files['file']

    if not file.filename.endswith('.xlsx'):
        return jsonify({"message": "文件类型错误，只支持Excel文件"}), 400

    try:
        # 读取所有工作表
        dfs = pd.read_excel(file, sheet_name=None)
        required_columns = {'student_id', 'name', 'department', 'role_in_depart', 'tel', 'password'}

        for sheet_name, df in dfs.items():
            # 检查当前工作表是否包含必要的列
            if not required_columns.issubset(df.columns):
                return jsonify({"message": f"工作表 '{sheet_name}' 缺少必要的列"}), 400

            for _, row in df.iterrows():
                row['password']=str(row['password'])
                row['password']=hashlize(row['password'])
                row['password']=row['password'].decode('utf8')
                s=Student(student_id=row['student_id'],name=row['name'],tel=row['tel'],department=row['department'],role_in_depart=row['role_in_depart'],pswd_hash=row['password'])
                db.session.add(s)
        db.session.commit()
        return jsonify({"message": "用户导入成功"}), 200

    except Exception as e:
        logging.error(f"发生错误: {str(e)}")
        return jsonify({"message": f"导入用户失败: {str(e)}"}), 500

