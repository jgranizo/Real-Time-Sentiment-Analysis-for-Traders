from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)