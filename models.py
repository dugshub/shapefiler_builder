# models.py
import geojson
from marshmallow.fields import Nested, Str, List
from marshmallow_geojson import GeoJSONSchema, PropertiesSchema, FeatureSchema, FeatureCollectionSchema
from sqlalchemy.orm import Mapped, mapped_column

from config import db, ma, DATAPATH


class ShapefileBuilder():
    def __init__(self, wof_id):
        self.id = wof_id
        self.shapefile_path = self._get_filepath()
        self.geom: GeoJSONSchema

    def createMaplayerObject(self):
        with open(self.shapefile_path) as f:
            wof_json = geojson.load(f)

        geometry = wof_json['geometry']
        self.geom = geometry
        bounding_box = wof_json['bbox']
        name = wof_json['properties']['wof:name']
        hierarchy = wof_json['properties']['wof:hierarchy']
        parent_id = wof_json['properties']['wof:parent_id']
        shape_type = wof_json['properties']['wof:placetype']
        locality = wof_json['properties']['wof:hierarchy'][0].get('locality_id')

        return self.createShapefile(
            geometry=geometry,
            bounding_box=bounding_box,
            name=name,
            # hierarchy=hierarchy,
            parent_id=parent_id,
            type=shape_type,
            locality=locality
        )

    def createShapefile(self, geometry, bounding_box, name, parent_id, type, locality):
        shape = Shapefile(
            id=self.id,
            name=name,
            # bounding_box=bounding_box,
            # geom=geometry,
            # hierarchy=hierarchy,
            shape_type=type,
            parent_id = locality
        )
        shape.bounding_box = bounding_box
        shape.geom = geometry
        shape.add_geos()
        return shape

    def _get_filepath(self):
        s = str(self.id)
        id_path = f'{DATAPATH}' + s[:3] + '/' + s[3:6] + '/' + s[6:9] + '/' + s[9:] + '/'
        return id_path + s + '.geojson'


#         sqla_session = db.sess
class Shapefile(db.Model):
    __tablename__ = 'shapefile'

    id: Mapped[int] = mapped_column(primary_key=True, init=True)
    name: Mapped[str] = mapped_column(init=True)
    shape_type: Mapped[str] = mapped_column(init=True)
    parent_id: Mapped[str] = mapped_column(init=True)
    # bounding_box: Mapped[str]
    # geom: Mapped[str]
    # hierarchy: str
    bounding_box = None
    properties = None
    feature = None
    geometry = None
    geom = None

    def add_geos(self):
        self.properties = property_schema.dump(self)
        self.geometry = geojson_schema.dump(self.geom)
        self.feature = feature_schema.dump(self)

    def _get_geojson_format(self):
        geometry = self.geometry
        properties = self.properties

        geometry.update(properties)
        return geometry


class ShapefilePropertySchema(PropertiesSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shapefile
        fields = ('id', 'name')


class ShapefileFeatureSchema(FeatureSchema, ma.SQLAlchemyAutoSchema):
    type = Str(
        default='Feature',
    )
    properties = Nested(
        ShapefilePropertySchema,
        required=True,
    )


class ShapefileGeoJSONSchema(GeoJSONSchema, ma.SQLAlchemyAutoSchema):
    feature_schema = ShapefileFeatureSchema


class ShapefileFeatureCollectionSchema(FeatureCollectionSchema, ma.SQLAlchemyAutoSchema):
    type = Str(
        default='FeatureCollection',
    )
    features = List(
        Nested(ShapefileFeatureSchema()),
        required=True,
    )


# class Neighbourhood(Shapefile):
#     __tablename__ = "neighbourhood"
#     id :Mapped[int] = mapped_column(ForeignKey('shapefile.id'), primary_key=True)
#     neighbourhood_name: Mapped[str]


geojson_schema = ShapefileGeoJSONSchema()
property_schema = ShapefilePropertySchema()
feature_schema = ShapefileFeatureSchema()
features_schema = ShapefileFeatureSchema(many=True)
featurecollection_schema = ShapefileFeatureCollectionSchema()
