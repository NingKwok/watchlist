"""A tiny Flask app for a personal watchlist.

This module creates a Flask application and defines a single route
('/') which returns a welcome message. The comments are in Chinese to
explain the code for learning purposes.
"""

from flask import Flask

# 创建 Flask 应用实例。传入 __name__ 以便 Flask 能找到静态文件和模板的路径。
app = Flask(__name__)

@app.route('/')  # 将下面的函数绑定到根 URL ('/')
def hello():
    """根路由的视图函数：返回欢迎信息字符串。"""
    # 返回的字符串会作为 HTTP 响应的主体发送给客户端
    return "Welcome to my watchlist."