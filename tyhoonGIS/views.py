from tyhoonGIS import app, db
from flask import Flask, render_template, request, redirect, url_for,flash
from tyhoonGIS.models import Typhoon,User
#编辑视图函数
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        name = request.form.get('name')  # 传入表单对应输入字段的 name 值
        ename = request.form.get('ename')
        begin_time = request.form.get('begin_time')
        end_time = request.form.get('end_time')
        t=Typhoon(name=name, ename=ename, begin_time=begin_time, end_time=end_time)

        db.session.add(t)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    typhoons= Typhoon.query.all()
    return render_template('index.html', Typhoons=typhoons)
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码