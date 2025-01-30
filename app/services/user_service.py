from app.core.security import hash_password, verify_password
from app.models import User  # Assuming you have a User model

def register_user(username, password):
    hashed_pw = hash_password(password)
    # Save user in database
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and verify_password(user.password, password):
        return user
    return None
