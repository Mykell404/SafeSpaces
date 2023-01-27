from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
                                        os.path.join(base_dir, 'users.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '53e929ba4f69ad675b05e2e8'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"User {self.username}"


# class Post(db.Model):
#     __tablename__ = "posts"
#     id = db.Column(db.Integer(), primary_key=True)
#     post_title = db.Column(db.String(80), nullable=False)
#     post = db.Column(db.String(), nullable=False)
#     created_by = db.Column(db.String(), db.ForeignKey('user.username'), nullabe=False)
#     pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"{self.post_title} written by {self.created_by}"


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


