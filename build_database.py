from config import app, db, reporting_markets
from models import Shapefile, ShapefileBuilder
import shapefile
from sqlalchemy import select


def build_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.app_context():
        for market_id in reporting_markets:
            db.session.add(ShapefileBuilder(market_id).createMaplayerObject())
        db.session.commit()

    with app.app_context():
        stmt = select(Shapefile).where(Shapefile.shape_type=='locality')
        markets = db.session.execute(stmt).scalars().all()
        market_ids = [market.id for market in markets]

    all_neighbourhoods = shapefile._get_related_ids(market_filter=market_ids)

    neighbourhoods = [ShapefileBuilder(neighbourhood).createMaplayerObject() for neighbourhood in all_neighbourhoods]
    with app.app_context():
        [db.session.add(neighbourhood) for neighbourhood in neighbourhoods]
        db.session.commit()


if __name__ == '__main__':
    build_db()
    populate_db()
