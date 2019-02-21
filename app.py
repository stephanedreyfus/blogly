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


@app.route('/')
def redirect_to_users():
    '''redirect to list of users'''
    return redirect('/users')


@app.route('/users/new')
def add_user_form():
    '''shows add user form'''
    return render_template("add_user_form.html")


@app.route('/users', methods=['POST'])
def process_user_form():
    '''gather data from from and send to database'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form.get('img_url') or None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users')
def show_list_of_users():
    ''' shows all users with links to their profiles, have button
    to go to add user form page '''

    user_list = User.query.all()

    return render_template('users_list.html', user_list=user_list)


@app.route('/users/<int:id>')
def user_page(id):
    ''' Dynamically shows user pages. '''

    user = User.query.get(id)

    return render_template('user_page.html',
                           id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           img_url=user.img_url)
