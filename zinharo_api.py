from zinharo_api import app, db
from zinharo_api.models import Client

def make_db():
    """Makes a basic db with admin user"""

    db.create_all()

if __name__ == "__main__":
    #make_db()

    app.run(host="0.0.0.0", port=8082)
