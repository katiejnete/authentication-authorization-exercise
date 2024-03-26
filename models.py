"""Models for Flask Feedback."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
import sqlalchemy.exc


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)


bcrypt = Bcrypt()


class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register_user(cls, username, password, email, first_name, last_name):
        """Hashes password for new user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return user

    @classmethod
    def authenticate_user(cls, username, password):
        """Authenticate user."""

        try:
            user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
            
            if user and bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return "Incorrect password."
        except sqlalchemy.exc.NoResultFound:
            return "Incorrect username."
        
    @classmethod
    def find_user(cls, feedback_id):
        """Find user with feedback id."""
        try:
            return db.session.query(cls).join(Feedback).filter(Feedback.id == feedback_id).one()
        except sqlalchemy.exc.NoResultFound:
            return None

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'))

    @classmethod
    def get_user_feedback(cls, username):
        """Get all of user's feedback."""
        try:
            return db.session.query(cls).join(User).filter(cls.username == username).all()
        except sqlalchemy.exc.NoResultFound:
            return None