from flask import Flask, request, jsonify, render_template
import json
import nltk
from nltk.corpus import words

app = Flask(__name__)
nltk.download('words')
word_list = set(words.words())

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

@app.route('/add_word', methods=['POST'])
def add_word():
    word = request.form['word'].strip().lower()
    database = load_database()
    
    if word in database['words']:
        return jsonify({'status': 'error', 'message': 'Word already exists in the database.'})
    
    if not is_valid_word(word):
        return jsonify({'status': 'error', 'message': 'Invalid word.'})
    
    database['words'].append(word)
    save_database(database)
    return jsonify({'status': 'success', 'message': 'Word added to the database.'})

if __name__ == '__main__':
    app.run(debug=True) 