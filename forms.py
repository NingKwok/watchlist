"""表单定义模块

本模块定义了电影看板应用中使用的所有表单类。
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class MovieForm(FlaskForm):
    """电影表单类

    用于添加和编辑电影信息的表单，包含以下字段：
    - title: 电影标题（必填）
    - year: 上映年份（必填，正整数）
    - genre: 电影类型（必填，下拉选择）
    - rating: 评分（必填，1-10）
    - notes: 备注（可选）
    - cover_image: 封面图片（可选）
    - remove_cover: 删除封面（仅编辑时有效）
    - submit: 提交按钮
    """

    # 电影标题 - 必填字段
    title = StringField('电影标题', validators=[DataRequired(message='电影标题不能为空')])

    # 上映年份 - 必填，且必须是正整数（使用 NumberRange 限制）
    year = IntegerField('上映年份', validators=[
        DataRequired(message='上映年份不能为空'),
        NumberRange(min=1888, message='请输入有效的年份（不早于 1888 年）')
    ])

    # 电影类型 - 必填，提供下拉选择
    genre = SelectField('电影类型', choices=[
        ('动作', '动作'),
        ('科幻', '科幻'),
        ('剧情', '剧情'),
        ('喜剧', '喜剧'),
        ('恐怖', '恐怖'),
        ('动画', '动画'),
        ('其他', '其他')
    ], validators=[DataRequired(message='请选择电影类型')])

    # 评分 - 必填，范围 1-10
    rating = IntegerField('评分（1-10）', validators=[
        DataRequired(message='评分不能为空'),
        NumberRange(min=1, max=10, message='评分必须在 1 到 10 之间')
    ])

    # 备注 - 可选字段
    notes = TextAreaField('备注')

    # 封面图片上传 - 可选，允许的图片格式
    cover_image = FileField('封面图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'],
                    '只支持 JPG, JPEG, PNG, GIF, WEBP 格式的图片')
    ])

    # 删除封面 - 仅用于编辑模式
    remove_cover = BooleanField('删除当前封面图片')

    # 提交按钮
    submit = SubmitField('保存')
