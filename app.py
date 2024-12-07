from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
from datetime import date
import nltk
from nltk.corpus import words
import ssl
import certifi
import json
import random
import os

ssl._create_default_https_context = ssl._create_unverified_context
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
nltk_data_dir = os.path.join('/tmp', 'nltk_data')
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(nltk_data_dir)
instance_path = os.path.join(os.getcwd(), 'instance')
os.makedirs(instance_path, exist_ok=True)
app = Flask(__name__, instance_path=instance_path)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "users.db")}'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# API KEY
MW_API_KEY = 'bff29416-af74-4873-bf21-fb2971ee7a56'
def is_blacklisted(word, blacklist):
    return word.lower() in blacklist
def contains_forbidden_keyword(username, keywords):
    return any(keyword in username.lower() for keyword in keywords)
word_list = set(words.words())
definition_cache = {}
blacklisted_words = ["badword1", "badword2", "badword3"]
forbidden_keywords = ["admin", "root", "superuser"]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    contributions = db.Column(db.Text, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    word_coins = db.Column(db.Integer, nullable=False, default=0)
    achievements = db.Column(db.Text, nullable=True, default="")
    words_entered_today = db.Column(db.Integer, nullable=False, default=0)
    last_word_entry_date = db.Column(db.Date, nullable=True)

class WordOfTheDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def check_and_award_achievements(user):
    achievements = user.achievements.split(',') if user.achievements else []
    contributions_count = len(user.contributions.split(',')) if user.contributions else 0

    new_achievements = []

    if contributions_count >= 1 and 'First Contribution' not in achievements:
        new_achievements.append({'name': 'First Contribution', 'image': url_for('static', filename='images/achievements/first_contribution.png')})

    if contributions_count >= 10 and '10 Contributions' not in achievements:
        new_achievements.append({'name': '10 Contributions', 'image': url_for('static', filename='images/achievements/ten_contributions.png')})

    if contributions_count >= 20 and '20 Contributions' not in achievements:
        new_achievements.append({'name': '20 Contributions', 'image': url_for('static', filename='images/achievements/twenty_contributions.png')})
    if new_achievements:
        achievements.extend([ach['name'] for ach in new_achievements])
        user.achievements = ','.join(achievements)
        db.session.commit()
        flash(f'New achievements unlocked: {", ".join([ach["name"] for ach in new_achievements])}', 'success')
    return new_achievements
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import json

def load_database():
    try:
        with open('words_database.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"words": []}
    except FileNotFoundError:
        return {"words": []}
def save_database(data):
    with open('words_database.json', 'w') as file:
        json.dump(data, file, indent=4)

def is_valid_word(word):
    return word in word_list

def get_word_definition(word):
    if word in definition_cache:
        return definition_cache[word]
    placeholder_definition = "This is a placeholder definition."
    definition_cache[word] = placeholder_definition
    return placeholder_definition

def get_word_of_the_day():
    today = date.today()
    word_of_the_day_entry = WordOfTheDay.query.filter_by(date=today).first()
    
    if word_of_the_day_entry:
        word = word_of_the_day_entry.word
    else:
        database = load_database()
        if not database['words']:
            return None, None, None
        word = random.choice(database['words'])
        new_word_of_the_day = WordOfTheDay(word=word, date=today)
        db.session.add(new_word_of_the_day)
        db.session.commit()
    
    user = User.query.filter(User.contributions.like(f"%{word}%")).first()
    definition = get_word_definition(word)
    return word, user.username if user else "Unknown", definition

@app.route('/')
def index():
    users = User.query.all()
    leaderboard_data = sorted(users, key=lambda user: len(user.contributions.split(',')) if user.contributions else 0, reverse=True)
    word_of_the_day, discovered_by, definition = get_word_of_the_day()
    return render_template('index.html', leaderboard=leaderboard_data, word_of_the_day=word_of_the_day, discovered_by=discovered_by, definition=definition)

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
@app.route('/shop')
@login_required
def shop():
    items = [
        {'name': 'Background Color', 'cost': 50, 'type': 'background_color'},
        {'name': 'Profile Badge', 'cost': 100, 'type': 'profile_badge'},
    ]
    return render_template('shop.html', items=items, word_coins=current_user.word_coins)

@app.route('/redeem', methods=['POST'])
@login_required
def redeem():
    item_type = request.form['item_type']
    item_cost = int(request.form['item_cost'])
    
    if current_user.word_coins >= item_cost:
        current_user.word_coins -= item_cost
        db.session.commit()
        flash('Item redeemed successfully!', 'success')
    else:
        flash('Not enough Word Coins.', 'danger')
    
    return redirect(url_for('shop'))

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    contributions = user.contributions.split(',') if user.contributions else []
    return render_template('user_profile.html', user=user, contributions=contributions)

@app.route('/full_contributions/<int:user_id>')
@login_required
def full_contributions(user_id):
    user = User.query.get_or_404(user_id)
    contributions = user.contributions.split(',') if user.contributions else []
    return render_template('full_contributions.html', contributions=contributions, user=user)

@app.route('/word_game')
@login_required
def word_game():
    database = load_database()
    words = random.sample(database['words'], 5)  
    definitions = [get_word_definition(word) for word in words]
    word_definitions = list(zip(words, definitions))
    random.shuffle(word_definitions) 
    return render_template('word_game.html', word_definitions=word_definitions)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        users = User.query.filter(User.username.contains(search_query)).all()
        return render_template('search_results.html', users=users, search_query=search_query)
    return render_template('search.html')
@app.route('/add_word', methods=['POST'])
def add_word():
    try:
        if not current_user.is_authenticated:
            return jsonify({'status': 'error', 'message': 'Please sign in to add a word.'})
        
        word = request.form['word'].strip().lower()
        database = load_database()
        
        if is_blacklisted(word, blacklisted_words):
            return jsonify({'status': 'error', 'message': 'Invalid word.'})
        
        if word in database['words']:
            return jsonify({'status': 'error', 'message': 'Word already exists in the database.'})
        if not is_valid_word(word):
            return jsonify({'status': 'error', 'message': 'Invalid word.'})
        
        if current_user.last_word_entry_date != date.today():
            current_user.words_entered_today = 0
            current_user.last_word_entry_date = date.today()
        
        if current_user.words_entered_today >= 100:  
            return jsonify({'status': 'error', 'message': 'You have reached the daily limit for entering words.'})
        
        database['words'].append(word)
        save_database(database)
        
        if current_user.contributions:
            current_user.contributions += f',{word}'
        else:
            current_user.contributions = word
        current_user.word_coins += 10
        current_user.words_entered_today += 1
        db.session.commit()
        
        new_achievements = check_and_award_achievements(current_user)
        
        return jsonify({'status': 'success', 'message': 'Word added to the database.', 'new_achievements': new_achievements})
    except Exception as e:
        app.logger.error(f"Error in add_word function: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while adding the word.'})
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        if contains_forbidden_keyword(username, forbidden_keywords):
            flash('Invalid username.', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('profile'))
    
    return render_template('signup.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        if username and contains_forbidden_keyword(username, forbidden_keywords):
            flash('Invalid username.', 'danger')
            return redirect(url_for('settings'))
        
        if username:
            current_user.username = username
        if password:
            current_user.password = password
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)