from flask import Flask, render_template, request, redirect, url_for
from db.init import get_db_session
from db.models import Shoe, Size, Brand, User

app = Flask(__name__)
session = get_db_session()

@app.route('/')
def index():
    nome = request.args.get('nome', None)
    marca = request.args.get('marca', None)
    prezzo_max = request.args.get('prezzo_max', None)
    prezzo_min = request.args.get('prezzo_min', None)
    taglia = request.args.get('taglia', None)

    shoes_query = Shoe.get_shoes_query(session)
    sizes = Size.get_all(session)
    brands = Brand.get_all(session)

    if nome is not None and nome != '':
        shoes_query = Shoe.filter_by_name(shoes_query, nome)

    if marca is not None and marca != '':
        shoes_query = Shoe.filter_by_brand(shoes_query, marca)

    if taglia is not None and taglia != '':
        try:
            t = int(taglia)
            shoes_query = Shoe.filter_by_size(shoes_query, t)
        except ValueError:
            print("Valore non valido di taglia")

    if prezzo_min:
        try:
            p_min = float(prezzo_min)
            shoes_query = Shoe.filter_by_price_min(shoes_query, p_min)
        except ValueError:
            print('Valore non valido di prezzo_min')

    if prezzo_max:
        try:
            p_max = float(prezzo_max)
            shoes_query = Shoe.filter_by_price_max(shoes_query, p_max)
        except ValueError:
            print('Valore non valido di prezzo_max')

    shoes = Shoe.finalize_query(shoes_query)
    return render_template('index.html', shoes=shoes, brands=brands, sizes=sizes,
                           marca=marca, prezzo_max=prezzo_max, prezzo_min=prezzo_min, taglia=taglia,
                           nome=nome)

@app.route('/shoe/<int:shoe_id>')
def shoe_detail(shoe_id):
    shoe = session.query(Shoe).get(shoe_id)
    if not shoe:
        return "Scarpa non trovata", 404
    return render_template('shoe_detail.html', shoe=shoe)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')

    if request.method == 'POST':
        name = request.form.get('nome')
        surname = request.form.get('cognome')
        email = request.form.get('email')

        nuovo_contatto = User(name=name, surname=surname, email=email)
        session.add(nuovo_contatto)
        session.commit()
        return redirect(url_for('contact_success'))


@app.route('/contact_success')
def contact_success():
    return render_template('message.html', title='Conferma', message='Contatto inviato correttamente')

@app.route('/about')
def about():
    return render_template('message.html', title='Chi siamo',
                           message= 'Questo progetto è stato sviluppato da Dalila Aprile.<br>Grazie per averlo visualizzato!')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
