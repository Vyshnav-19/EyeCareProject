from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return "<h1>Hii This is Home Page..............</h1>"


@views.route('/c')
def check():
    return "<h1>Hello</h1>"
