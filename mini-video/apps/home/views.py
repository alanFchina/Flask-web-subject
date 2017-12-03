import os
import uuid

from apps import app
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
from .forms import RegisterForm, LoginForm, UserDetailForm, PwdForm, CommentForm
from functools import wraps
from apps.models import User, UserLog, Preview, Tag, Movie, Comment, Moviecol
from apps import db
from werkzeug.utils import secure_filename
from apps.admin.views import change_filename


# 登录需求装饰器
def user_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return func(*args, **kwargs)
    return decorated_function


# 会员登录
@home.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["account"]).first()
        if not user:
            flash("用户还未注册", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["pwd"]):
            flash("密码错误", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id

        # 存入登录日志
        user_log = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(user_log)
        db.session.commit()

        return redirect(url_for("home.index", page=1))
    return render_template('home/login.html', form=form)


# 会员注销
@home.route('/logout/')
@user_login_req
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 会员注册
@home.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            email=data["email"],
            phone=data["phone"],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功,请登录!", "ok")
        return redirect(url_for("home.login"))
    return render_template("home/register.html", form=form)


# 会员中心
@home.route('/user/', methods=["GET", "POST"])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(session["user_id"])
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data.filename:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!enctype = "multipart/form-data"
            file_face = secure_filename(form.face.data.filename)

            face_dir = os.path.join(app.config["UP_DIR"], "user")

            if not os.path.exists(face_dir):
                os.makedirs(face_dir)
                os.chmod(face_dir, "rw")
            user.face = change_filename(file_face)
            form.face.data.save(os.path.join(face_dir, user.face))

        # 昵称,邮箱,手机号码唯一性判断STAR
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在", "err")
            return redirect(url_for("home.user"))
        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已被注册", "err")
            return redirect(url_for("home.user"))
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash("手机号已被注册", "err")
            return redirect(url_for("home.user"))
        # 唯一性判断END

        user.name = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.info = data["info"]
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route('/pwd/', methods=["GET", "POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.get(session["user_id"])
        if not user.check_pwd(data["old_pwd"]):
            flash("原密码错误!", "err")
            return redirect(url_for("home.pwd"))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.commit()
        flash("修改密码成功, 请重新登录", "ok")
        session.pop("user", None)
        session.pop("user_id", None)
        return redirect(url_for("home.login"))
    return render_template("home/pwd.html", form=form)


# 评论记录
@home.route('/comments/<int:page>/')
@user_login_req
def comments(page=1):
    page_data = Comment.query.join(User).filter(
        User.id == Comment.user_id,
        Comment.user_id == session['user_id']
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_data=page_data)


# 添加电影收藏
@home.route("/moviecol/add/<int:id>", methods=["GET"])
@user_login_req
def moviecol_add(id=None):
    movie = Movie.query.get_or_404(id)
    movie_col = Moviecol(
        movie_id=id,
        user_id=session["user_id"]
    )
    db.session.add(movie_col)
    db.session.commit()
    flash("收藏电影成功", "ok")
    return redirect(url_for("home.play", id=id, page=1))


# 收藏电影
@home.route('/moviecol/<int:page>')
@user_login_req
def moviecol(page=1):
    page_data = Moviecol.query.join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        Moviecol.user_id == session["user_id"]
    ).order_by(
        Moviecol.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', page_data=page_data)


# 登录日志
@home.route('/loginlog/<int:page>/', methods=["GET", "POST"])
@user_login_req
def login_log(page=None):
    if not page:
        page = 1
    page_data = UserLog.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        UserLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 首页
@home.route("/", methods=["GET"])
def first():
    return redirect(url_for("home.index", page=1))


@home.route('/<int:page>/', methods=["GET"])
def index(page=1):
    tags = Tag.query.all()
    tid = request.args.get("tid", 0)

    page_data = Movie.query
    if int(tid):
        page_data = page_data.filter_by(tag_id=int(tid))
    star = request.args.get("star", 0)
    if int(star):
        page_data = page_data.filter_by(star=int(star))
    # if not int(tid) and not int(star):
    #     page_data = page_data.all()
    time = request.args.get("time", 0)
    if int(time):
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.add_time.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.add_time.desc()
            )
    pm = request.args.get("pm", 0)
    if int(pm):
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.play_num.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.play_num.desc()
            )
    cm = request.args.get("cm", 0)
    if int(cm):
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.comment_num.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.comment_num.desc()
            )

    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    page_data = page_data.paginate(page=page, per_page=12)
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


# 上映预告轮播图
@home.route('/animation/', methods=["GET"])
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


# 查找
@home.route('/search/<int:page>/', methods=["GET"])
def search(page=1):
    key = request.args.get("key", "")
    page_data = Movie.query.filter(
        Movie.title.ilike("%" + key + "%")
    ).order_by(
        Movie.add_time.desc()
    ).paginate(page=page, per_page=10)
    nums = len(page_data.items)
    return render_template('home/search.html', key=key, nums=nums, page_data=page_data)


# 播放电影
@home.route('/play/<int:id>/<int:page>', methods=["GET", "POST"])
def play(id=None, page=1):
    form = CommentForm()
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == id
    ).first_or_404()
    if request.method == "GET":
        movie.play_num += 1
    if session["user"] and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        movie.comment_num += 1
        db.session.commit()
        flash("发表评论成功", "ok")
        return redirect(url_for("home.play", id=id, page=page))
    db.session.commit()

    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id,
        Movie.id == id
    )
    comment_num = page_data.count()
    page_data = page_data.order_by(Comment.add_time.desc()).paginate(page=page, per_page=5)

    return render_template('home/play.html', movie=movie, form=form, page_data=page_data, comment_num=comment_num)
