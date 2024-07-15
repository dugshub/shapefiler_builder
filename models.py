# models.py
from sqlalchemy.orm import Mapped, mapped_column

from config import db ,ma


class Shapefile(db.Model):
    __tablename__ = 'shapefiles'

    id: Mapped[int] = mapped_column(primary_key=True,init=True)
    name: Mapped[str] = mapped_column(init=False)
    filepath: Mapped[str] = mapped_column(init=False)
    bounding_box: Mapped[str] = mapped_column(init=False)
    parent_id: Mapped[str] = mapped_column(init=False)
    shape_type: Mapped[str] = mapped_column(init=False)

class ShapefileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shapefile
        load_instance = True
#         sqla_session = db.session

shapefile_schema = ShapefileSchema()
shapefiles_schema = ShapefileSchema(many=True)

