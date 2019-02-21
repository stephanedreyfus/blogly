"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    
    user_list = User.query.order_by(User.id.desc()).all()
    
    return render_template('users_list.html', user_list=user_list)


@app.route('/users/<int:id>')
def user_page(id):
    ''' Dynamically shows user pages. '''

    user = User.query.get(id)
    posts = user.posts
    
    return render_template('user_page.html',
                           id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           img_url=user.img_url,
                           posts=posts)


@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    ''' delete user '''
    found_user = User.query.get(id)
    db.session.delete(found_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:id>/edit')
def edit_user_page(id):
    ''' Show user details for editing '''

    user = User.query.get(id)

    return render_template('edit_user_page.html',
                           id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           img_url=user.img_url)


@app.route('/users/<int:id>/edit', methods=['POST'])
def edit_user_info(id):
    ''' Update user information'''

    user = User.query.get(id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form.get('img_url') or None

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:id>/posts/new')
def add_post(id):
    ''' Shows form to write post '''

    user = User.query.get(id)

    return render_template('add_post_form.html',
                           id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name)


@app.route('/users/<int:id>/post', methods=["POST"])
def commit_post(id):
    ''' submits post to database '''

    title = request.form['post_title']
    content = request.form['post_content']

    new_post = Post(title=title,
                    content=content,
                    user_id=id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    ''' show post with delete, back, and edit buttons'''

    post = Post.query.get(post_id)
    user = post.user

    return render_template('read_post.html',
                           user=user,
                           post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    ''' post deletion'''
    found_post = Post.query.get(post_id)

    db.session.delete(found_post)
    db.session.commit()

    return redirect(f'/users/{found_post.user_id}')
