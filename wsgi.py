from app import app, db
from waitress import serve

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)