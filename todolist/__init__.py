from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_keycloak import Keycloak
from flask_keycloak.auth import AuthError
from flask_graphql import GraphQLView


app = Flask(__name__)
app.config['SECRET_KEY'] = '9b9e7dbea0fb86674dc3dec509b35e40'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from todolist import routes

keycloak = Keycloak(app)
app.add_url_rule('/graphql', view_func=keycloak.protect(GraphQLView.as_view('graphql', schema=schema, graphiql=True)))

def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response