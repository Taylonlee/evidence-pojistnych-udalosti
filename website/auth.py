from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

# Vytvoření blueprintu pro autentizaci
auth = Blueprint('auth', __name__)

# Definice cesty pro přihlášení
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Zpracování odeslaného formuláře
    if request.method == 'POST':
        email = request.form.get('email')
        heslo = request.form.get('heslo')

        # Vyhledání uživatele podle emailu
        user = User.query.filter_by(email=email).first()
        if user:
            # Kontrola hesla
            if check_password_hash(user.heslo, heslo):
                flash('Uživatel přihlášen', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Nesprávný uživatel nebo heslo!', category='error')
        else:
            flash('Nesprávný uživatel nebo heslo!', category='error')

    # Zobrazení šablony pro přihlášení
    return render_template("login.html", user=current_user)

# Definice cesty pro odhlášení
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Definice cesty pro registraci
@auth.route('/sign-up', methods=['GET', 'POST'])
def register():
    # Zpracování odeslaného formuláře
    if request.method == 'POST':
        email = request.form.get('email')
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        heslo1 = request.form.get('heslo1')
        heslo2 = request.form.get('heslo2')

        # Kontrola existence uživatele s daným emailem
        user = User.query.filter_by(email=email).first()

        valid_input = True

        # Kontrola platnosti vstupů
        if len(email) < 4:
            flash('Email musí mít víc než 4 znaky.', category='error')
            valid_input = False
        if len(jmeno) < 2:
            flash('Křestní jméno musí mít víc než 2 znaky.', category='error')
            valid_input = False
        if len(prijmeni) < 2:
            flash('Přijmení musí mít víc než 2 znaky.', category='error')
            valid_input = False
        if heslo1 != heslo2:
            flash('Hesla se neshodují.', category='error')
            valid_input = False
        if len(heslo1) < 7:
            flash('Heslo musí mít víc než 7 znaků.', category='error')
            valid_input = False

        # Přidání nového uživatele do databáze
        elif valid_input:
            try:
                new_user = User(email=email, jmeno=jmeno, prijmeni=prijmeni,
                                heslo=generate_password_hash(heslo1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Účet byl vytvořen!', category='success')
                return redirect(url_for('views.home'))
            except IntegrityError:
                db.session.rollback()
                flash('Zadaný email již existuje.', category='error')

    # Zobrazení šablony pro registraci
    return render_template("register.html", user=current_user)