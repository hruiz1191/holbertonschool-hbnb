# app/web/views.py

from flask import Blueprint, render_template

# Crea un Blueprint llamado 'web'
web = Blueprint('web', __name__)

# Ruta principal: lista de lugares
@web.route('/')
def index():
    return render_template('index.html')

# Ruta para login
@web.route('/login')
def login():
    return render_template('login.html')

# Ruta para ver detalles de un lugar (recibe el id del lugar)
@web.route('/places/<place_id>')
def place_details(place_id):
    return render_template('place.html')

# Ruta para añadir un review (NO recibe place_id en la URL)
@web.route('/add_review')
def add_review():
    return render_template('add_review.html')
