from app import create_app
from app.config.connect import db

app = create_app()

if __name__ == '__main__':
    # Create database tables if they don't exist yet
    with app.app_context():
        db.create_all()
    app.run(debug=True)
