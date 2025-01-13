import os
from script import app, db, Word
from nltk.corpus import words
from datetime import datetime, timezone  

def populate_word_table():
    word_list = words.words()
    with app.app_context():
        for word in word_list:
            word = word.lower()
            if not Word.query.filter_by(word=word).first():
                new_word = Word(word=word, date_added=datetime.now(timezone.utc))
                db.session.add(new_word)
        db.session.commit()
    print("Word table populated with NLTK words.")

if __name__ == "__main__":
    populate_word_table()