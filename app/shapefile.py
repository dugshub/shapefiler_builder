# shapefile.py
from random import randrange
from typing import List

from sqlalchemy import select

from config import df, reporting_markets, excluded_shapefiles, ignored_geo_shapes, app, db, config
from models import ShapefileBuilder, features_schema, featurecollection_schema, Shapefile


## Read reporting Markets ##


def _get_related_ids(accepted_shapes=('neighbourhood',), market_filter=reporting_markets):
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
    print(f"{len(ids)} shapefiles were mapped across {len(markets)} reporting markets.")
    # [print(market.name) for market in reporting_markets]
    return ids


def get_shapefiles_by_ids(ids: List[int]):
    shapefile_objs: list[Shapefile] = [ShapefileBuilder(id).createMaplayerObject() for id in ids]
    shape_features = features_schema.dump(shapefile_objs)

    class Meta:
        type = 'FeatureCollection'
        features = shape_features

    geojson_file = featurecollection_schema.dump(Meta)
    return geojson_file


def _get_related_shapefiles(market_filter=[None]):
    ids = _get_related_ids(market_filter=market_filter)
    shapefile_objs: list[Shapefile] = [ShapefileBuilder(key).createMaplayerObject() for key, val in ids.items()]

    ##add filter to split out shapefiles by type
    shape_features = features_schema.dump(shapefile_objs)

    class Meta:
        type = 'FeatureCollection'
        features = shape_features

    geojson_file = featurecollection_schema.dump(Meta)
    return geojson_file


def get_neighbourhoods_by_locality_id(locality_id):
    with app.app_context():
        stmt = select(Shapefile).where(Shapefile.shape_type == 'locality')
        markets = db.session.execute(stmt).scalars().all()
        given_market = db.session.get(Shapefile, locality_id)

    markets = [market.id for market in markets]

    if not given_market:
        market = markets[randrange(5)]

    else:
        market = given_market.id

    with app.app_context():
        stmt = select(Shapefile).filter(Shapefile.parent_id == market).where(Shapefile.shape_type == 'neighbourhood')
        neighbourhoods = db.session.execute(stmt).scalars().all()

    neighbourhood_ids = [neighbourhood.id for neighbourhood in neighbourhoods]
    return get_shapefiles_by_ids(neighbourhood_ids)


def get_shapefiles(market_filter=reporting_markets):
    shapefile_objs = _get_related_shapefiles(market_filter)
    return shapefile_objs
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

def get_reporting_markets():
    return config['reporting_markets']