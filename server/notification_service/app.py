from notification_service import create_app, db
from notification_service.config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)

    with app.test_request_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8080)
