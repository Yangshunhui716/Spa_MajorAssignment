from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "fjhghdfvgsfjnvnkd"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Yangshunhui%40167@localhost/spaappdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3

cloudinary.config(
  	cloud_name = "databreak",
  	api_key = "143511745215512",
  	api_secret = "f35MCfbdfoIhB8Z6XSrQVTmGQBA"
)

db = SQLAlchemy(app)