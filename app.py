from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify
import os
from flask import render_template
from flask_migrate import Migrate
from flask import redirect
from flask import url_for

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:akhil123@localhost:5432/book_suggestion"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserBookSuggestions(db.Model):
    __tablename__ = 'UserBookSuggestions'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=False, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    book_title = db.Column(db.String(80), unique=True, nullable=False)
    book_author = db.Column(db.String(80), unique=True, nullable=True)

    def __init__(self, user_name, user_email, book_title, book_author):
        self.user_name = user_name
        self.user_email = user_email
        self.book_title = book_title
        self.book_author = book_author

    # def __repr__(self):
    #     return f"Book {self.book_title}"


# db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == "POST":
            data = request.form
            new_book = UserBookSuggestions(user_name=data['user_name'],
                                           user_email=data['user_email'],
                                           book_title=data['book_title'],
                                           book_author=data.get('book_author', None)
                                           )
            db.session.add(new_book)
            db.session.commit()
            print('data saved successfully...')
            return redirect(url_for('show_books'))
        else:
            return render_template('home.html')
    except Exception as inst:
        return render_template('error.html')


@app.route('/books', methods=['GET'])
def show_books():
    try:
        books = UserBookSuggestions.query.all()
        results = [
            {
                "user_name": data.user_name,
                "user_email": data.user_email,
                "book_title": data.book_title,
                "book_author": data.book_author
            } for data in books]
        return render_template('book_list.html', books=results)
    except Exception as inst:
        return render_template('error.html')




