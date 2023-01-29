from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
                                        os.path.join(base_dir, 'users.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '53e929ba4f69ad675b05e2e8'

db = SQLAlchemy(app)

login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"User {self.username}"

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer(), primary_key=True)
    post_title = db.Column(db.String(80), nullable=False)
    post = db.Column(db.String(), nullable=False)
    created_by = db.Column(db.Integer(), db.ForeignKey('users.id'))
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.post_title} written by {self.created_by}"


@app.route('/')
def index():
    posts = Post.query.all()

    context = {
        'posts': posts
    }
    db.create_all()
    return render_template('index.html', **context)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('register'))

        email_exist = User.query.filter_by(email=email).first()
        if email_exist:
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post_title = request.form.get('post-title')
        post = request.form.get('post')
        created_by = current_user.id

        new_post = Post(post_title=post_title, post=post, created_by=created_by)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
