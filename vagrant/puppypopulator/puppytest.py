from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def allPuppies():
	return session.query(Puppy).order_by(Puppy.name.desc()).all()

# for puppy in allPuppies():
	# print puppy.name

def youngPuppy():
	today = datetime.date.today()
	days_old = 30*6
	birth_day = today - datetime.timedelta(days = days_old)
	return session.query(Puppy).filter(Puppy.dateOfBirth > birth_day).order_by(Puppy.dateOfBirth.desc()).all()



def allPuppiesAscWeight():
	return session.query(Puppy).order_by(Puppy.weight).all()

# for puppy in allPuppiesAscWeight():
# 	print 'weight:', puppy.weight

# print "count:", session.query(func.count(Puppy.id)).one()[0]

# for puppy in youngPuppy():
# 	print puppy.dateOfBirth

def gropyedPyppies():
	return session.query(func.count(Puppy.id), Shelter.name).join(Puppy.shelter ).group_by(Puppy.shelter_id).all()

for puppy in gropyedPyppies():
	print puppy

