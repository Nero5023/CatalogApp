from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def listAllRestaurant():
	restaurants = session.query(Restaurant).all()
	# names = []
	# for restaurant in restaurants:
	# 	names.append(restaurant.name)
	# return 
	return restaurants
 
def createNewRestaurant(new_name):
	new_resaturant = Restaurant(name=new_name)
	session.add(new_resaturant)
	session.commit()

def restaurantWithID(ID):
	restaurant = session.query(Restaurant).filter_by(id = ID).one()
	return restaurant
	
def updateRestaurant(new_restaurant):
	session.add(new_restaurant)
	session.commit()

def deleteRestaurantWithID(ID):
	restaurantToDelete = restaurantWithID(ID)
	session.delete(restaurantToDelete)
	session.commit()