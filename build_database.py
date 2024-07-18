from config import db, app
import models

def build_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    build_db()