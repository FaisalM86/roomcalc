# auth.py
# Authentication and authorization module for the RoomCalc application

import bcrypt
from sqlalchemy.orm import sessionmaker

from data_access import create_session
from models import User, Base
from sqlalchemy import create_engine
from config import DATABASE_NAME

# Create an engine that stores data in the local directory's database file.
engine = create_engine('sqlite:///' + DATABASE_NAME)

# Create a Session class with automatic transactions
Session = sessionmaker(bind=engine)

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def create_user(username, password):
    """Create a new user with a hashed password"""
    hashed_password = hash_password(password)
    session = Session()
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()

def authenticate_user(username, password):
    """Authenticate a user and return True if correct"""
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and verify_password(user.password, password):
        return True
    return False

def change_user_password(username, old_password, new_password):
    """Change user password if old password is correct"""
    if authenticate_user(username, old_password):
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        user.password = hash_password(new_password)
        session.commit()
        session.close()
        return True
    return False

def delete_user(username):
    """Delete a user from the database"""
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return True
    return False

def authorize_user(username, required_access_level):
    """Authorize a user based on access level"""
    session = create_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and user.access_level >= required_access_level:
        return True
    return False
