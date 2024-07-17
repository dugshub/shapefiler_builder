# models.py
import geojson
from marshmallow.fields import Nested, Str, List
from marshmallow_geojson import GeoJSONSchema, PropertiesSchema, FeatureSchema, FeatureCollectionSchema
from sqlalchemy.orm import Mapped, mapped_column

from config import db, ma


class Shapefile():
    def __init__(self, wof_id, filepath):
        self.id = wof_id
        self.shapefile_path = filepath

    def createMaplayerObject(self):
        with open(self.shapefile_path) as f:
            wof_json = geojson.load(f)

        geometry = wof_json['geometry']
        bounding_box = wof_json['bbox']
        name = wof_json['properties']['wof:name']
        hierarchy = wof_json['properties']['wof:hierarchy']
        parent_id = wof_json['properties']['wof:parent_id']
        shape_type = wof_json['properties']['wof:placetype']

        if shape_type == 'neighbourhood':
            return self.createNeighbourhood(
                geometry=geometry,
                bounding_box=bounding_box,
                name=name,
                hierarchy=hierarchy,
                parent_id=parent_id
            )

    def createNeighbourhood(self, geometry, bounding_box, name, hierarchy, parent_id):
        return Neighbourhood(
            id=self.id,
            name=name,
            bounding_box=bounding_box,
            geom=geometry,
            hierarchy=hierarchy
        )


#         sqla_session = db.sess
class Neighbourhood(db.Model):
    __tablename__ = 'neighbourhoods'

    id: Mapped[int] = mapped_column(primary_key=True, init=True)
    name: Mapped[str] = mapped_column(init=True)
    bounding_box: Mapped[str] = mapped_column(init=True)
    geom: Mapped[str]
    hierarchy: str

    def __post_init__(self):
        self.properties = property_schema.dump(self)
        self.geometry = geojson_schema.dump(self.geom)
        self.feature = feature_schema.dump(self)

    def _get_geojson_format(self):
        geometry = self.geometry
        properties = self.properties

        geometry.update(properties)
        print(geometry)
        return geometry


class ShapefilePropertySchema(PropertiesSchema, ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Neighbourhood
        fields = ('id', 'name','bounding_box')


class ShapefileFeatureSchema(FeatureSchema,ma.SQLAlchemyAutoSchema):
    type = Str(
            default='Feature',
        )
    properties = Nested(
        ShapefilePropertySchema,
        required=True,
    )



class ShapefileGeoJSONSchema(GeoJSONSchema, ma.SQLAlchemyAutoSchema):
    feature_schema = ShapefileFeatureSchema

class ShapefileFeatureCollectionSchema(FeatureCollectionSchema,ma.SQLAlchemyAutoSchema):
    type = Str(
        default='FeatureCollection',
    )
    features = List(
        Nested(ShapefileFeatureSchema()),
        required=True,
    )


geojson_schema = ShapefileGeoJSONSchema()
property_schema = ShapefilePropertySchema()
feature_schema = ShapefileFeatureSchema()
features_schema = ShapefileFeatureSchema(many=True)
featurecollection_schema = ShapefileFeatureCollectionSchema()
