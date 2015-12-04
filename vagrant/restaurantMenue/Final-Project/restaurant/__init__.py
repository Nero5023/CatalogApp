from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurant.database_setup import Base
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

import restaurant.views