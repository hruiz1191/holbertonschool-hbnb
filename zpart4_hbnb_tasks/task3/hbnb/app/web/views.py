from flask import Blueprint, render_template
from app.models.place import Place
import os

web = Blueprint(
    'web',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../../templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../../static')
)

@web.route('/')
def index():
    places = Place.query.all()
    return render_template('index.html', places=places)

@web.route('/login')
def login():
    return render_template('login.html')

@web.route('/places/<place_id>')
def place_details(place_id):
    return render_template('place.html')  # <-- Esta realmente ahora no se usa (pero la puedes dejar por si acaso luego haces flask directo)

@web.route('/place.html')  # <-- ESTA ES LA CLAVE para arreglar tu error
def place_html():
    return render_template('place.html')

@web.route('/add_review')
def add_review():
    return render_template('add_review.html')
