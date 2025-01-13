from script import app, db, User

def update_achievements():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.achievements is None:
                user.achievements = ""
        db.session.commit()
        print("Achievements updated for all users.")

if __name__ == "__main__":
    update_achievements()