from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy  # Import Flask-SQLAlchemy
from datetime import datetime
from . import db
from flask_login import UserMixin


class Outbreaks(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Country = db.Column(db.Text)
    iso2 = db.Column(db.Text)
    iso3 = db.Column(db.Text)
    Year = db.Column(db.Integer)
    icd10n = db.Column(db.Text)
    icd103n = db.Column(db.Text)
    icd104n = db.Column(db.Text)
    icd10c = db.Column(db.Text)
    icd103c = db.Column(db.Text)
    icd104c = db.Column(db.Text)
    icd11c1 = db.Column(db.Text)
    icd11c2 = db.Column(db.Text)
    icd11c3 = db.Column(db.Text)
    icd11l1 = db.Column(db.Text)
    icd11l2 = db.Column(db.Text)
    icd11l3 = db.Column(db.Text)
    Disease = db.Column(db.Text)
    DONs = db.Column(db.Text)
    Definition = db.Column(db.Text)
    search_timestamp = Column(DateTime, default=datetime.utcnow)


class Search(db.Model):
    # Define the Search model for storing search events
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each search
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to associate with the
    # User model
    country = db.Column(db.String, nullable=False)  # Country selected in the search
    year = db.Column(db.Integer, nullable=False)  # Year selected in the search
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when the search occurred


class User(db.Model, UserMixin):
    # Define the User model
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    searches = db.relationship('Search', backref='user', lazy=True)  # Relationship to the Search model, lazy loading

    # Add a method to get user's search history
    def get_search_history(self):
        return Search.query.filter_by(user_id=self.id).order_by(Search.timestamp.desc()).all()

