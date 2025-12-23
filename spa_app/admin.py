from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from spa_app.models import DichVu
from spa_app import app, db

admin = Admin(app=app, name="SPA_APP", theme=Bootstrap4Theme())

admin.add_view(ModelView(DichVu, db.session))