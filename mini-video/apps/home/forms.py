from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from apps.models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称!"),
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
            "required": "required"
        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱"),
            Email("请输入正确的邮箱格式")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
            "required": "required"
        }
    )

    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入昵称!"),
            Regexp(r"1[34578]\d{9}", message="手机格式不正确")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired("请再次输入密码!"),
            EqualTo("pwd", "密码不一致")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请确认密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user:
            raise ValidationError("昵称已被注册")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user:
            raise ValidationError("邮箱已被注册")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user:
            raise ValidationError("手机号码已被注册")


class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号!"),
        ],
        description="账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "用户名/邮箱/手机号码",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!"),
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )


class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称!"),
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
            "required": "required"
        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱"),
            Email("请输入正确的邮箱格式")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
            "required": "required"
        }
    )

    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入昵称!"),
            Regexp(r"1[34578]\d{9}", message="手机格式不正确")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码",
            "required": "required"
        }
    )

    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像!")
        ],
        description="头像",
        render_kw={
            "id": "input_face"
        }
    )

    info = TextAreaField(
        label="简介",
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )

    submit = SubmitField(
        "保存修改",
        render_kw={
            "class": "btn btn-success"
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='原密码',
        validators=[
            DataRequired("请输入原密码!")
        ],
        description="原密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入原密码",
            "required": "required",
            "id": "input_oldpwd"
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码!")
        ],
        description="新密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入新密码",
            "required": "required",
            "id": "input_newpwd"
        }
    )

    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-success btn-lg"
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请填写评论内容!")
        ],
        description="评论内容",
        render_kw={
            "id": "input_content"
        }
    )

    submit = SubmitField(
        "提交评论",
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )