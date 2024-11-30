from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import nltk
from nltk.corpus import words

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

nltk.download('words')
word_list = set(words.words())

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    contributions = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_database():
    with open('words_database.json', 'r') as file:
        return json.load(file)

def save_database(data):
    with open('words_database.json', 'w') as file:
        json.dump(data, file, indent=4)

def is_valid_word(word):
    return word in word_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('profile'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    contributions = current_user.contributions.split(',') if current_user.contributions else []
    return render_template('profile.html', contributions=contributions)

@app.route('/add_word', methods=['POST'])
@login_required
def add_word():
    word = request.form['word'].strip().lower()
    database = load_database()
    
    if word in database['words']:
        return jsonify({'status': 'error', 'message': 'Word already exists in the database.'})
    if not is_valid_word(word):
        return jsonify({'status': 'error', 'message': 'Invalid word.'})
    
    database['words'].append(word)
    save_database(database)
    
    if current_user.contributions:
        current_user.contributions += f',{word}'
    else:
        current_user.contributions = word
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Word added to the database.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)