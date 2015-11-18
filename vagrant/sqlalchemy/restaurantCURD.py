from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def listAllRestaurant():
	restaurants = session.query(Restaurant).all()
	names = []
	for restaurant in restaurants:
		names.append(restaurant.name)
	return names
 
def createNewRestaurant(new_name):
	new_resaturant = Restaurant(name=new_name)
	session.add(new_resaturant)
	session.commit()
	

print listAllRestaurant()