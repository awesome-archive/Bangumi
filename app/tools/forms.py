# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models.crud import Database


class LoginForm(Form):
    name = StringField(
        "账号",
        validators=[
            DataRequired("账号不能为空！")
        ]
    )

    pwd = PasswordField(
        "密码",
        validators=[
            DataRequired("密码不能为空！")
        ]
    )

    def validate_name(self, field):
        if len(field.data) > 14:
            raise ValidationError("用户名长度过长！")

        data = Database.user_unique(field.data)
        if not data:
            raise ValidationError("账号不存在！")

    def validate_pwd(self, field):
        if len(field.data) > 14:
            raise ValidationError("密码长度过长！")

        data = Database.check_login(self.name.data, field.data)
        if not data:
            raise ValidationError("密码不正确！")


class RegistForm(Form):
    name = StringField(
        "昵称",
        validators=[
            DataRequired('昵称不能为空！')
        ]
    )

    pwd = PasswordField(
        "密码",
        validators=[
            DataRequired("密码不能为空！")
        ]
    )

    repwd = PasswordField(
        "确认密码",
        validators=[
            DataRequired("确认密码不能为空！"),
            EqualTo('pwd', message="两次输入密码不一致！")
        ]
    )

    email = StringField(
        "邮箱",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ]
    )

    phone = StringField(
        "手机",
        validators=[
            DataRequired("手机不能为空！"),
            Regexp("1[345789]\\d{9}", message="手机格式不正确！")
        ]
    )

    def validate_name(self, field):
        if len(field.data) > 14:
            raise ValidationError("用户名长度过长！")

        data = Database.user_unique(field.data)
        if data:
            raise ValidationError("昵称已经存在！")

    def validate_email(self, field):
        data = Database.user_unique(field.data, 2)
        if data:
            raise ValidationError("邮箱已经存在！")

    def validate_phone(self, field):
        data = Database.user_unique(field.data, 3)
        if data:
            raise ValidationError("手机已经存在！")

    def validate_pwd(self, field):
        if len(field.data) > 14:
            raise ValidationError("密码长度过长！")


class UserProfileEditForm(Form):
    id = IntegerField(
        "编号",
        validators=[
            DataRequired("编号不能为空！")
        ]
    )

    face = StringField(
        "头像",
        validators=[
            DataRequired("头像不能为空！")
        ]
    )

    info = StringField(
        "个性签名",
        validators=[
            DataRequired("个性签名不能为空！")
        ]
    )

    sex = IntegerField(
        "性别",
        validators=[
            DataRequired("性别不能为空！")
        ]
    )

    xingzuo = IntegerField(
        "星座",
        validators=[
            DataRequired("星座不能为空！")
        ]
    )

    def validate_info(self, field):
        if len(field.data) > 200:
            raise ValidationError("个性签名长度过长！")


class InsertForm(Form):
    name = StringField(
        "标题",
        validators=[
            DataRequired("标题不能为空！")
        ]
    )

    logo = StringField(
        "封面",
        validators=[
            DataRequired("封面不能为空！")
        ]
    )

    links = StringField(
        "链接",
        validators=[
            DataRequired("链接不能为空！")
        ]
    )

    actors = StringField(
        "演员",
        validators=[
            DataRequired("演员不能为空！")
        ]
    )

    tags = StringField(
        "标签",
        validators=[
            DataRequired("标签不能为空！")
        ]
    )

    director = StringField(
        "导演",
        validators=[
            DataRequired("导演不能为空！")
        ]
    )

    area = StringField(
        "地区",
        validators=[
            DataRequired("地区不能为空！")
        ]
    )

    language = StringField(
        "语言",
        validators=[
            DataRequired("语言不能为空！")
        ]
    )

    year = StringField(
        "年份",
        validators=[
            DataRequired("年份不能为空！")
        ]
    )

    status = StringField(
        "状态",
        validators=[
            DataRequired("状态不能为空！")
        ]
    )

    desc = StringField(
        "描述",
        validators=[
            DataRequired("描述不能为空！")
        ]
    )

    vclass = StringField(
        "分类",
        validators=[
            DataRequired("分类不能为空！")
        ]
    )


class EditForm(Form):
    id = StringField(
        "编号",
        validators=[
            DataRequired("编号不能为空！")
        ]
    )

    name = StringField(
        "标题",
        validators=[
            DataRequired("标题不能为空！")
        ]
    )

    logo = StringField(
        "封面",
        validators=[
            DataRequired("封面不能为空！")
        ]
    )

    links = StringField(
        "链接",
        validators=[
            DataRequired("链接不能为空！")
        ]
    )

    actors = StringField(
        "演员",
        validators=[
            DataRequired("演员不能为空！")
        ]
    )

    tags = StringField(
        "标签",
        validators=[
            DataRequired("标签不能为空！")
        ]
    )

    director = StringField(
        "导演",
        validators=[
            DataRequired("导演不能为空！")
        ]
    )

    area = StringField(
        "地区",
        validators=[
            DataRequired("地区不能为空！")
        ]
    )

    language = StringField(
        "语言",
        validators=[
            DataRequired("语言不能为空！")
        ]
    )

    year = StringField(
        "年份",
        validators=[
            DataRequired("年份不能为空！")
        ]
    )

    status = StringField(
        "状态",
        validators=[
            DataRequired("状态不能为空！")
        ]
    )

    desc = StringField(
        "描述",
        validators=[
            DataRequired("描述不能为空！")
        ]
    )

    vclass = StringField(
        "分类",
        validators=[
            DataRequired("分类不能为空！")
        ]
    )


class ChatForm(Form):
    vid = StringField(
        "视频编号",
        validators=[
            DataRequired("视频编号不能为空！")
        ]
    )

    sv = StringField(
        "子视频编号",
        validators=[
            DataRequired("子视频编号不能为空！")
        ]
    )


class GbookForm(Form):
    name = StringField(
        "用户",
        validators=[
            DataRequired("用户名不能为空！")
        ]
    )

    content = StringField(
        "内容",
        validators=[
            DataRequired("留言内容不能为空！")
        ]
    )

    chkcode = StringField(
        "验证码",
        validators=[
            DataRequired("验证码不能为空！")
        ]
    )

    def validate_content(self, field):
        if len(field.data) > 500:
            raise ValidationError("留言内容过长！")
