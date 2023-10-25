from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # Vytvoření instance Flask aplikace
    app = Flask(__name__)
    # Nastavení tajného klíče pro ochranu dat
    app.config['SECRET_KEY'] = 'totojetajnyklic'
    # Nastavení cesty k databázi
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # Inicializace databáze s aplikací
    db.init_app(app)

    # Import modulů views a auth
    from .views import views
    from .auth import auth

    # Registrace modulů views a auth jako blueprintů
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import modelů User, Client a Pojisteni
    from .models import User, Client, Pojisteni

    # Vytvoření databáze v kontextu aplikace
    with app.app_context():
        db.create_all()

    # Inicializace správce přihlášení
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Načtení uživatele z databáze podle jeho ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
