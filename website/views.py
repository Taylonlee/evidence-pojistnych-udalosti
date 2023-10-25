from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_paginate import Pagination
from website.models import Client, Pojisteni
from website import db
from datetime import datetime

# Vytvoření blueprintu pro zobrazení
views = Blueprint('views', __name__)

# Definice cesty pro domovskou stránku
@views.route('/pojisteni-app', methods=['GET', 'POST'])
@views.route('/', methods=['GET', 'POST'])
def home():
    # Zobrazení šablony pro domovskou stránku
    return render_template("home.html", user=current_user)

# Cesta pro zobrazení formuláře pro přidání nového pojištěnce
@views.route('/pojisteni-app/pojistenci/novy')
@login_required
def novy_pojistenec():
    return render_template("novy_pojistenec.html", user=current_user)

# Cesta pro zpracování odeslaného formuláře a uložení nového pojištěnce
@views.route('/pojisteni-app/pojistenci/novy', methods=['GET','POST'])
def pridat_pojistence():
    # Zpracování odeslaného formuláře
    if request.method == 'POST':
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        datum_narozeni = datetime.strptime(request.form.get('datum_narozeni'), "%Y-%m-%d").date()
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        ulice = request.form.get('ulice')
        cp = request.form.get('cp')
        mesto = request.form.get('mesto')
        psc = request.form.get('psc')

        valid_input = True
        # Kontrola platnosti vstupů
        if len(jmeno) == 0 or len(prijmeni) == 0:
            flash('Musí být vyplněno Jméno a Příjmení pojištěnce!', category='error')
            valid_input = False
        if len(telefon) == 0 and len(email) == 0:
            flash('Musí být vyplněné kontaktní údaje (Telefon nebo Email)!', category='error')
            valid_input = False
        if len(ulice) == 0 or len(cp) == 0:
            flash('Chybí Ulice a Číslo popisné!', category='error')
            valid_input = False
        if len(mesto) == 0:
            flash('Není vyplněno Město!', category='error')
            valid_input = False
        if len(psc) == 0:
            flash('Není vyplněn PSČ!', category='error')
            valid_input = False

        elif valid_input:
            new_client = Client(jmeno=jmeno, prijmeni=prijmeni, datum_narozeni=datum_narozeni,
                                telefon=telefon, email=email,
                                ulice=ulice, cp=cp, mesto=mesto, psc=psc,
                                user_id=current_user.id)
            db.session.add(new_client)
            db.session.commit()
            flash('Pojištěnec byl uložen.', category='success')
            return redirect(url_for('views.zobrazit_pojistenci'))
        return render_template("novy_pojistenec.html", user=current_user)

@views.route('/pojisteni-app/pojistenci', methods=['GET', 'POST'])
def zobrazit_pojistenci():
    # Získání aktuální stránky
    page = int(request.args.get('page', 1))
    # Nastavení počtu záznamů na stránce
    per_page = 3
    offset = (page - 1) * per_page
    # Získání všech pojištěnců pro aktuálního uživatele
    pojistenci = Client.query.filter_by(user_id=current_user.id).all()
    # Výpočet celkového počtu pojištěnců
    total = len(pojistenci)
    pojistenci_strankovani = pojistenci[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template("pojistenci.html", user=current_user, pojistenci=pojistenci_strankovani, page=page,
                           per_page=per_page, pagination=pagination)

@views.route('/pojisteni-app/pojistenci/smazat/<int:id>', methods=['POST'])
def smazat_pojistence(id):
    # Hledání pojištěnce podle ID
    pojistenec = Client.query.get_or_404(id)
    # Smazání pojištěnce z databáze
    db.session.delete(pojistenec)
    db.session.commit()
    flash('Pojištěnec byl smazán.', category='success')
    return redirect(url_for('views.zobrazit_pojistenci'))

@views.route('/pojisteni-app/pojistenci/upravit/<int:id>', methods=['GET', 'POST'])
def upravit_pojistence(id):
    # Hledání pojištěnce podle ID
    pojistenec = Client.query.get_or_404(id)
    if request.method == 'POST':
        # Aktualizace údajů pojištěnce
        pojistenec.jmeno = request.form['jmeno']
        pojistenec.prijmeni = request.form['prijmeni']
        pojistenec.datum_narozeni = datetime.strptime(request.form.get('datum_narozeni'), "%Y-%m-%d").date()
        pojistenec.telefon = request.form['telefon']
        pojistenec.email = request.form['email']
        pojistenec.ulice = request.form['ulice']
        pojistenec.mesto = request.form['mesto']
        pojistenec.psc = request.form['psc']
        db.session.commit()
        flash('Pojištěnec byl upraven.', category='success')
        return redirect(url_for('views.detail_pojistence', id=pojistenec.id))
    return render_template('upravit_pojistence.html', pojistenec=pojistenec, user=current_user)

@views.route('/pojisteni-app/pojistenci/detail/<int:id>', methods=['GET', 'POST'])
def detail_pojistence(id):
    # Hledání pojištěnce podle ID
    pojistenec = Client.query.get_or_404(id)
    # Získání pojištění pro daného pojištěnce
    pojisteni_list = Pojisteni.query.filter_by(client_id=pojistenec.id).all()
    return render_template('detail_pojistence.html', pojistenec=pojistenec,
                           pojisteni_list=pojisteni_list, user=current_user)

@views.route('/pojisteni-app/pojisteni', methods=['GET','POST'])
def zobrazit_pojisteni():
    return render_template('pojisteni.html', user=current_user)

@views.route('/pojisteni-app/pojistenci/novy/<int:id>', methods=['GET', 'POST'])
def pridat_pojisteni(id):
    # Hledání pojištěnce podle ID
    pojistenec = Client.query.get_or_404(id)
    # Zpracování odeslaného formuláře
    if request.method == 'POST':
        nazev = request.form['nazev']
        castka = request.form['castka']
        predmet = request.form['predmet']
        platnost_od = datetime.strptime(request.form['platnost_od'], "%Y-%m-%d").date()
        platnost_do = datetime.strptime(request.form['platnost_do'], "%Y-%m-%d").date()
        # Kontrola, zda je částka ve správném formátu
        try:
            castka = int(castka)
        except ValueError:
            flash('Chyba: Vložte platnou částku.', category='error')
            return render_template('nove_pojisteni.html', user=current_user, pojistenec=pojistenec)

        nove_pojisteni = Pojisteni(nazev=nazev, castka=castka, predmet=predmet,
                                   platnost_od=platnost_od, platnost_do=platnost_do, client_id=pojistenec.id)
        db.session.add(nove_pojisteni)
        db.session.commit()
        flash('Pojištění bylo přidáno.', category='success')
        return redirect(url_for('views.detail_pojistence', id=pojistenec.id))
    return render_template('nove_pojisteni.html', user=current_user, pojistenec=pojistenec)

@views.route('/pojisteni-app/pojisteni/smazat/<int:id>', methods=['GET', 'POST'])
def smazat_pojisteni(id):
    # Hledání pojištění podle ID
    pojisteni = Pojisteni.query.get_or_404(id)
    # Získání ID pojištěnce
    pojistenec_id = pojisteni.client_id
    # Smazání pojištění z databáze
    db.session.delete(pojisteni)
    db.session.commit()
    flash('Pojištění bylo smazáno.', category='success')
    return redirect(url_for('views.detail_pojistence', id=pojistenec_id))

@views.route('/pojisteni-app/pojisteni/upravit/<int:client_id>/<int:pojisteni_id>', methods=['GET', 'POST'])
def upravit_pojisteni(client_id, pojisteni_id):
    # Hledání pojištěnce podle ID
    pojistenec = Client.query.get_or_404(client_id)
    # Hledání pojištění podle ID
    pojisteni = Pojisteni.query.get_or_404(pojisteni_id)
    if request.method == 'POST':
        # Aktualizace údajů u pojištění
        pojisteni.nazev = request.form['nazev']
        pojisteni.castka = request.form['castka']
        pojisteni.predmet = request.form['predmet']
        pojisteni.platnost_od = datetime.strptime(request.form['platnost_od'], "%Y-%m-%d").date()
        pojisteni.platnost_do = datetime.strptime(request.form['platnost_do'], "%Y-%m-%d").date()
        db.session.commit()
        flash('Pojištění bylo upraveno.', category='success')
        return redirect(url_for('views.detail_pojistence', id=client_id))
    return render_template('upravit_pojisteni.html', pojisteni=pojisteni, user=current_user,
                            pojistenec=pojistenec)