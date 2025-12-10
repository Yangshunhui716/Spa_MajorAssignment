from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key ="afebwjgfwlakngkaw"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/spaappdb?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 2

cloudinary.config(cloud_name ='dpkydyf9p',
                  api_key='451754462215985',
                  api_secret='wP3ub5rTqrFwpA4qzZSH0N3zxQs' )

db = SQLAlchemy(app)
login_manager = LoginManager(app)
