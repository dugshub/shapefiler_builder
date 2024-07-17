import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import load_spatialite

from sqlalchemy.event import listen
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)


class Base(MappedAsDataclass,DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'placetypes.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
ma = Marshmallow(app)

with app.app_context():
    db.drop_all()
    db.create_all()
