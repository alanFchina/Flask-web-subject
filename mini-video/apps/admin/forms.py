from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from apps.models import Admin, Tag, Auth, Role

tags = Tag.query.all()
auths_list = Auth.query.all()
role_list = Role.query.all()


class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号!")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
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
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account)
        if not admin:
            raise ValidationError("账号不存在!")


class TagForm(FlaskForm):
    """
    添加标签表单验证
    """

    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签!")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称!",
            "required": "required"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    """
    电影表单
    """
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名!")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名!",
            "required": "required"
        }
    )

    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件!")
        ],
        description="文件",
        render_kw={
            "id": "input_url"
        }
    )

    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired("请填写简介!")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": 10,
            "required": "required"
        }
    )

    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面!")
        ],
        description="封面",
        render_kw={
            "id": "input_logo"
        }
    )

    star = SelectField(
        label='星级',
        validators=[
            DataRequired("请选择星级!")
        ],
        coerce=int,
        description="星级",
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control"
        }
    )

    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired("请选择标签!")
        ],
        coerce=int,
        description="标签",
        choices=[(v.id, v.name) for v in tags],
        render_kw={
            "class": "form-control"
        }
    )

    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区!")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区!",
            "required": "required"
        }
    )

    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长!")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长!",
            "required": "required"
        }
    )

    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间!")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
        }
    )

    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )


class PreviewForm(FlaskForm):
    """
    电影预告表单
    """
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题!")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题!",
            # "required": "required"
        }
    )

    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请选择封面!")
        ],
        description="预告封面 ",
    )

    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )


class PwdForm(FlaskForm):
    """
    修改密码表单
    """
    old_pwd = PasswordField(
        label='原密码',
        validators=[
            DataRequired("请输入原密码!")
        ],
        description="原密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入原密码",
            "required": "required"
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码!")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
            "required": "required"
        }
    )

    submit = SubmitField(
        "确定",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("原密码错误!")


class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称!")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称!",
            "required": "required"
        }
    )

    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址!")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址!",
            "required": "required"
        }
    )

    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称!")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称!",
            "required": "required"
        }
    )

    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限列表!")
        ],
        description="权限列表",
        coerce=int,
        choices=[(v.id, v.name) for v in auths_list],
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称!")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称!",
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
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    repwd = PasswordField(
        label='重复密码',
        validators=[
            DataRequired("请再次输入密码!"),
            EqualTo("pwd", "两次密码不一致")
        ],
        description="重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入密码",
            "required": "required"
        }
    )

    # is_super = SelectField(
    #     label="是否为超级管理员",
    #     validators=[
    #         DataRequired("请选择是否为超级管理员!")
    #     ],
    #     coerce=int,
    #     choices=[(0, "不是"), (1, "是")],
    #     description="是否为超级管理员",
    #     render_kw={
    #         "class": "form-control"
    #     }
    # )

    role_id = SelectField(
        label="所属角色",
        validators=[
            DataRequired("请选择所属角色!")
        ],
        description="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in role_list],
        render_kw={
            "class": "form-control"
        }
    )

    submit = SubmitField(
        "确定",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )