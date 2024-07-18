# shapefile.py
from config import df, reporting_markets, excluded_shapefiles, ignored_geo_shapes
from models import ShapefileBuilder, features_schema, featurecollection_schema

## Read reporting Markets ##



def _get_related_ids(accepted_shapes=('neighbourhood',),market_filter=reporting_markets):
    """
    Get all the neighbourhoods associated with the set of Reporitng Markets defined in the
    config file.
    :return:
    """

    markets = [market_id for market_id in reporting_markets if market_id in market_filter]
    print(type(reporting_markets))
    df2 = df[
        df['locality'].isin(markets) & df['shape_type'].isin(accepted_shapes) & ~df['geo_shape'].isin(
            ignored_geo_shapes) & df['is_superceded'].isin(['[]']) & ~df['source_geom'].isin(excluded_shapefiles)]

    ids = df2['path'].to_dict()
    print (f"{len(ids)} shapefiles were mapped across {len(markets)} reporting markets.")
    # [print(market.name) for market in reporting_markets]
    return ids



def _get_related_shapefiles(market_filter=[None]):
    ids = _get_related_ids(market_filter=market_filter)
    shapefiles = [ShapefileBuilder(key).createMaplayerObject() for key, val in ids.items()]

    ##add filter to split out shapefiles by type
    return shapefiles


def get_shapefiles(market_filter=None):

    market_filter = [85923517]
    shapefile_objs = _get_related_shapefiles(market_filter)
    shape_features = features_schema.dump(shapefile_objs)

    class Meta:
        type = 'FeatureCollection'
        features = shape_features

    geojson_file = featurecollection_schema.dump(Meta)
    return geojson_file

# def get_shapefiles():
#     shapefile_objs = _get_related_shapefiles()
#     shape_features = features_schema.dump(shapefile_objs)
#
#     class Meta:
#         type = 'FeatureCollection'
#         features = shape_features
#
#     geojson_file = featurecollection_schema.dump(Meta)
#     return geojson_file



