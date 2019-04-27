from app import create_app, db
from app.config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)

    with app.test_request_context():
        db.create_all()

    app.run(port=8080)
