from website import create_app
from website import db
from website.models import Note, Item, Group, User
from werkzeug.security import generate_password_hash, check_password_hash


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


