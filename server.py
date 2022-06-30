import os
import argparse
import secrets

from flask import Flask, render_template, request, session
from flask_login import LoginManager

from routing.login.routes import login_bp
from routing.home.routes import home_bp

from db import user_db as udb
from routing.login.user import User


# Flask app instance
app = Flask(__name__)

# obtain secret key from environment
app.secret_key = os.environ.get("SECRET_KEY")

# saves the database credentials into
# a more functional format
db = {
    'host': os.environ.get('HOST'),
    'user': os.environ.get('USER'),
    'pass': os.environ.get('PASS'),
    'database': os.environ.get('DATABASE'),
    'port': os.environ.get('PORT')
}

app.config['db'] = db

# login manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


# registers login Flask blueprints
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)


# user loader function
@login_manager.user_loader
def load_user(id):
    data = udb.get_by_user(id, db)
    return User(data['uuid'], data['username'], data['email'])


if __name__ == "__main__":
    # obtains host, username, password, database, and port from
    # command line for testing purposes only
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="Host for PostgreSQL development server", type=str)
    parser.add_argument('user', help="User for PostgreSQL development server", type=str)
    parser.add_argument('password', help="Password for PostgreSQL development server", type=str)
    parser.add_argument('db', help="Database for PostgreSQL development server", type=str)
    parser.add_argument('port', help="Port for PostgreSQL development server", type=int)

    args = parser.parse_args()

    db = {
        'host': args.host,
        'user': args.user,
        'pass': args.password,
        'database': args.db,
        'port': args.port
    }

    app.config['db'] = db

    # generate secret key for testing
    app.secret_key = secrets.token_urlsafe(32)

    app.run(debug=True)
