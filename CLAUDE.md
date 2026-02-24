# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

使用中文回复
我叫Viking

## Project Overview

这是一个个人电影看板 Flask Web 应用，用于记录和管理观看过的电影。

**已实现功能**：
- 电影的增删改查（CRUD）
- 电影封面图片上传
- 电影信息包括：标题、年份、类型、评分（1-10）、备注
- Bootstrap 5 界面

## Development Environment

- **Python Version**: 3.13.0
- **Virtual Environment**: `watchlist-venv/`
- **Main Framework**: Flask 3.1.2
- **ORM**: Flask-SQLAlchemy
- **Form Handling**: Flask-WTF
- **Database**: SQLite
- **Frontend**: Bootstrap 5 (CDN)

## Common Commands

### Running the Application
```bash
# 激活虚拟环境（Windows）
.\watchlist-venv\Scripts\activate

# 启动应用
flask run
```

或
```bash
python app.py
```

访问：http://127.0.0.1:5000

### Testing
```bash
python test.py
```

### Database Operations
```bash
# Flask shell
flask shell

# 初始化数据库（如需重建）
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

## Project Structure

```
watchlist/
├── app.py                  # 主应用文件（Flask 应用、路由、数据库模型）
├── forms.py                # 表单类定义（MovieForm）
├── test.py                 # 简单的测试脚本
├── .flaskenv               # Flask 环境配置文件
├── .env                    # 环境变量（不提交到 git）
├── uploads/                # 上传文件目录（不提交到 git）
│   └── covers/             # 电影封面图片存储目录
├── templates/              # Jinja2 模板目录
│   ├── base.html           # 基础模板（包含导航栏和 Bootstrap）
│   ├── index.html          # 首页（电影列表）
│   └── form.html           # 表单模板（添加/编辑电影）
├── watchlist.db            # SQLite 数据库文件（不提交到 git）
└── watchlist-venv/         # Python 虚拟环境（不提交到 git）
```

## Database Schema

### Movie 表

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| id | Integer | 主键 | - |
| title | String(100) | 电影标题 | ✅ |
| year | Integer | 上映年份 | ✅ |
| genre | String(20) | 电影类型 | ✅ |
| rating | Integer | 评分（1-10） | ✅ |
| notes | Text | 备注 | ❌ |
| cover_image | String(255) | 封面图片文件名 | ❌ |
| created_at | DateTime | 创建时间 | - |

## Routes

| 路由 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 首页，显示所有电影列表 |
| `/add` | GET, POST | 添加新电影 |
| `/edit/<int:id>` | GET, POST | 编辑电影 |
| `/delete/<int:id>` | POST | 删除电影 |
| `/uploads/<path:filename>` | GET | 提供上传文件的静态访问 |

## Code Comments

代码库包含中文注释用于学习目的。在修改或添加代码时，请保持与现有注释风格的一致性。

## Image Upload Configuration

- **存储位置**: `uploads/covers/`
- **允许格式**: JPG, JPEG, PNG, GIF, WEBP
- **文件大小限制**: 5MB
- **文件命名**: 时间戳 + 原始文件名（避免冲突）
- **自动清理**: 删除电影时自动删除关联图片

## Development Notes

1. 使用 SQLite 作为开发数据库，生产环境建议使用 PostgreSQL
2. 当前 SECRET_KEY 为开发环境配置，生产环境需更改
3. 上传目录 `uploads/` 已添加到 .gitignore
4. 数据库文件 `watchlist.db` 已添加到 .gitignore
