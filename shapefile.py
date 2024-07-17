# shapefile.py
from config import df, reporting_markets, excluded_shapefiles, ignored_geo_shapes
from models import Shapefile, features_schema, featurecollection_schema

## Read reporting Markets ##



def _get_related_ids(accepted_shapes=('neighbourhood',)):
    """
    Get all the neighbourhoods associated with the set of Reporitng Markets defined in the
    config file.
    :return:
    """
    df2 = df[
        df['locality'].isin(reporting_markets) & df['shape_type'].isin(accepted_shapes) & ~df['geo_shape'].isin(
            ignored_geo_shapes) & df['is_superceded'].isin(['[]']) & ~df['source_geom'].isin(excluded_shapefiles)]

    ids = df2['path'].to_dict()
    return ids


def _get_related_shapefiles():
    ids = _get_related_ids()
    shapefiles = [Shapefile(key, val).createMaplayerObject() for key, val in ids.items()]

    ##add filter to split out shapefiles by type
    return shapefiles


def get_shapefiles():
    shapefile_objs = _get_related_shapefiles()
    shapefile_objs = [shapefile_objs[0],shapefile_objs[1]]
    shape_features = features_schema.dump(shapefile_objs)

    class Meta:
        type = 'FeatureCollection'
        features = shape_features

    geojson_file = featurecollection_schema.dumps(Meta)
    print(geojson_file)
    return geojson_file


