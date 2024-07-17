import pathlib

import connexion
import yaml
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy.event import listen
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)


class Base(MappedAsDataclass, DeclarativeBase):
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

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

ignored_geo_shapes = ['Point']
excluded_shapefiles = ['zetashapes', 'quattroshapes']
wof_df = pd.read_csv("data/combined.csv", index_col="id")

df = wof_df[
    ['name', 'shape_type', 'locality', 'parent_id', 'is_superceded', 'cesessation', 'geo_shape', 'hierarchy',
     'source_geom', 'alt_geom', 'path']]

reporting_markets = [market['id'] for market in config['reporting_markets']]