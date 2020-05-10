from zinharo_api import app, db
from zinharo_api.models import Client

def make_db():
    """Makes a basic db with admin user"""

    db.create_all()

    admin_user = Client("admin", "qwerty123", "An admin user")

    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    # make_db()

    app.run(host="0.0.0.0", port=8080)
