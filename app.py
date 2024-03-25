"""Authentication Authorization Exercise"""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, Pet
from forms import AddPetForm
from secret import SECRET_KEY


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = SECRET_KEY