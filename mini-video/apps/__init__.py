import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:962899122@127.0.0.1:3306/mini-video'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '671f368dffe54ee089ab7411e56e909c'
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.debug = True
db = SQLAlchemy(app)

from apps.home import home as home_blueprint
from apps.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404