from datetime import datetime
from apps import db


class User(db.Model):
    """
    会员
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    userlogs = db.relationship("UserLog", backref='user')  # 会员日志外键关系
    comments = db.relationship("Comment", backref='user')  # 评论外键关系
    moviecols = db.relationship("Moviecol", backref='user')  # 收藏外键关系

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class UserLog(db.Model):
    """
    会员登录日志
    """
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录ip
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


class Tag(db.Model):
    """
        标签
    """
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    movies = db.relationship("Movie", backref="tag")  # 标签外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    """
    电影
    """
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.BigInteger)  # 播放量
    comment_num = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))  # 所属标题
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    comments = db.relationship("Comment", backref='movie')  # 评论外键关系
    moviecols = db.relationship("Moviecol", backref='movie')  # 收藏外键关系

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    """
    上映预告
    """
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    """
    用户评论
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户id
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


class Moviecol(db.Model):
    """
    电影收藏
    """
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户id
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


class Auth(db.Model):
    """
    权限
    """
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


class Role(db.Model):
    """
    角色
    """
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auths = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    admins = db.relationship("Admin", backref='role')  # 管理员外键关系

    def __repr__(self):
        return "<Role %r>" % self.name


class Admin(db.Model):
    """
    管理员
    """
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员, 1为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员日志外键关系
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作外键关系

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class Adminlog(db.Model):
    """
    管理员登陆日志
    """
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Adminlog %r>' % self.id


class Oplog(db.Model):
    """
    操作日志
    """
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Oplog %r>' % self.id


# if __name__ == "__main__":
#     # db.create_all()
#     # role = Role(
#     #     name="超级管理员",
#     #     auths=""
#     # )
#     # db.session.add(role)
#     # db.session.commit()
#     from werkzeug.security import generate_password_hash
#     admin = Admin(
#         name='imoocmovie',
#         pwd=generate_password_hash("imoocmovie"),
#         is_super=1,
#         role_id=1
#     )
#     db.session.add(admin)
#     db.session.commit()
