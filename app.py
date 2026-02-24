"""A tiny Flask app for a personal watchlist.

本模块创建一个 Flask 应用，提供个人电影看板功能。
功能包括：添加、查看、编辑和删除看过的电影，支持电影封面图片上传。
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'  # 用于表单 CSRF 保护

# 图片上传配置
# 上传文件夹路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'covers')
# 创建上传文件夹（如果不存在）
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 限制上传文件大小（最大 5MB）
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# 允许的图片文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """检查文件扩展名是否允许

    参数:
        filename: 文件名

    返回:
        bool: 如果文件扩展名允许则返回 True
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 创建 SQLAlchemy 数据库实例
db = SQLAlchemy(app)

# 数据库模型定义
class Movie(db.Model):
    """电影数据模型

    存储电影的详细信息，包括标题、年份、类型、评分、备注、封面图片等。
    """

    # 主键 ID
    id = db.Column(db.Integer, primary_key=True)

    # 电影标题（必填）
    title = db.Column(db.String(100), nullable=False)

    # 上映年份（必填）
    year = db.Column(db.Integer, nullable=False)

    # 电影类型（必填）
    genre = db.Column(db.String(20), nullable=False)

    # 评分（1-10，必填）
    rating = db.Column(db.Integer, nullable=False)

    # 备注（可选）
    notes = db.Column(db.Text)

    # 封面图片文件名（可选）
    cover_image = db.Column(db.String(255))

    # 创建时间（自动生成）
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        """返回模型的字符串表示"""
        return f'<Movie {self.title} ({self.year})>'


# 路由和视图函数定义
@app.route('/')
def index():
    """首页路由

    显示所有电影列表，按创建时间倒序排列（最新的在前）。
    """
    # 从数据库获取所有电影，按创建时间倒序排序
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    # 渲染首页模板
    return render_template('index.html', movies=movies)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """提供上传文件的静态访问

    参数:
        filename: 文件名
    """
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """添加电影路由

    GET: 显示添加电影表单
    POST: 处理表单提交，保存电影到数据库
    """
    from forms import MovieForm

    # 创建表单实例
    form = MovieForm()

    # 如果是 POST 请求且表单验证通过
    if form.validate_on_submit():
        # 处理封面图片上传
        cover_image_filename = None
        if form.cover_image.data and allowed_file(form.cover_image.data.filename):
            # 生成安全的文件名
            filename = secure_filename(form.cover_image.data.filename)
            # 添加时间戳前缀以避免文件名冲突
            from time import time
            unique_filename = f"{int(time())}_{filename}"
            # 保存文件
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            form.cover_image.data.save(filepath)
            cover_image_filename = unique_filename

        # 创建新的 Movie 实例
        movie = Movie(
            title=form.title.data,
            year=form.year.data,
            genre=form.genre.data,
            rating=form.rating.data,
            notes=form.notes.data,
            cover_image=cover_image_filename
        )
        # 添加到数据库会话
        db.session.add(movie)
        # 提交到数据库
        db.session.commit()
        # 显示成功提示
        flash('电影添加成功！', 'success')
        # 重定向到首页
        return redirect(url_for('index'))

    # GET 请求或表单验证失败，渲染表单页面
    return render_template('form.html', form=form, title='添加电影')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """编辑电影路由

    GET: 显示编辑电影表单，预填充现有数据
    POST: 处理表单提交，更新电影信息

    参数:
        id: 电影 ID
    """
    from forms import MovieForm

    # 根据 ID 查找电影，如果不存在则返回 404
    movie = Movie.query.get_or_404(id)
    # 记录旧封面文件名
    old_cover_image = movie.cover_image
    # 创建表单实例，使用现有数据填充
    form = MovieForm(obj=movie)

    # 如果是 POST 请求且表单验证通过
    if form.validate_on_submit():
        # 处理封面图片上传
        if form.cover_image.data:
            if allowed_file(form.cover_image.data.filename):
                # 生成安全的文件名
                filename = secure_filename(form.cover_image.data.filename)
                # 添加时间戳前缀以避免文件名冲突
                from time import time
                unique_filename = f"{int(time())}_{filename}"
                # 保存文件
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                form.cover_image.data.save(filepath)
                # 更新数据库中的文件名
                movie.cover_image = unique_filename

                # 删除旧的封面图片文件
                if old_cover_image:
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], old_cover_image)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
        else:
            # 如果没有上传新图片，且用户勾选了"删除封面"选项
            if request.form.get('remove_cover') == 'on':
                movie.cover_image = None
                # 删除旧的封面图片文件
                if old_cover_image:
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], old_cover_image)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)

        # 更新电影信息
        movie.title = form.title.data
        movie.year = form.year.data
        movie.genre = form.genre.data
        movie.rating = form.rating.data
        movie.notes = form.notes.data
        # 提交到数据库
        db.session.commit()
        # 显示成功提示
        flash('电影更新成功！', 'success')
        # 重定向到首页
        return redirect(url_for('index'))

    # GET 请求或表单验证失败，渲染表单页面
    return render_template('form.html', form=form, title='编辑电影', movie=movie)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """删除电影路由

    处理删除电影的 POST 请求，同时删除关联的封面图片文件。

    参数:
        id: 电影 ID
    """
    # 根据 ID 查找电影，如果不存在则返回 404
    movie = Movie.query.get_or_404(id)

    # 删除封面图片文件
    if movie.cover_image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], movie.cover_image)
        if os.path.exists(filepath):
            os.remove(filepath)

    # 从数据库删除
    db.session.delete(movie)
    # 提交到数据库
    db.session.commit()
    # 显示成功提示
    flash('电影删除成功！', 'success')
    # 重定向到首页
    return redirect(url_for('index'))


# 应用启动
if __name__ == '__main__':
    # 启动 Flask 开发服务器
    app.run(debug=True)
