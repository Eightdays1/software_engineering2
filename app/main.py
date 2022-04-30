from website import create_app

from website.views.views import views
from website.auth.auth import auth
from website.api.api import api

app = create_app()

app.register_blueprint(views)
app.register_blueprint(auth)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)


