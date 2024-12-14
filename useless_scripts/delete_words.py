from app import app, db
from app import Word  

def delete_all_words():
    with app.app_context():
        deleted = Word.query.delete()
        db.session.commit()
        print(f"Deleted {deleted} records from the Word table.")

if __name__ == "__main__":
    delete_all_words()