"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/users/new')
def add_user_form():
    return render_template("add_user_form.html")


@app.route('/users', methods=['POST'])
def process_user_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form.get('img_url')

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
