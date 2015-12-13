from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User
from datetime import datetime
from random import randint

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def randomTime():
	return datetime(2015, randint(3,12), randint(1,30), 
				randint(1,23), randint(1,59))


user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
	picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

category1 = Category(name = 'Soccer')

session.add(category1)
session.commit()

item1 = Item(name='Jersey', description='Description1', 
			date_time=randomTime(), category=category1, user=user1)
session.add(item1)
session.commit()

item2 = Item(name='Soccer Cleats', description='Description2',
			date_time=randomTime(), category=category1, user=user1)
session.add(item2)
session.commit()

item3 = Item(name='Two shinguards', description='Description3',
			date_time=randomTime(), category=category1, user=user1)
session.add(item3)
session.commit()

item4 = Item(name='Shinguards', description='Description4',
			date_time=randomTime(), category=category1, user=user1)
session.add(item4)
session.commit()

category2 = Category(name='Basketball')
session.add(category2)
session.commit()

category3 = Category(name='Baseball')
session.add(category3)
session.commit()

item5 = Item(name='Bat', description='Description5',
			date_time=randomTime(), category=category3, user=user1)
session.add(item5)
session.commit()

category4 = Category(name='Frisbee')
session.add(category4)
session.commit()

item6 = Item(name='Frisbee', description='Description6',
			date_time=randomTime(), category=category4, user=user1)
session.add(item6)
session.commit()

category5 = Category(name='Snowboarding')
session.add(category5)
session.commit()

item7 = Item(name='Googles', description='Description7',
			date_time=randomTime(), category=category5, user=user1)
session.add(item7)
session.commit()

item8 = Item(name='Snowboard', description='Description8',
			date_time=randomTime(), category=category5, user=user1)
session.add(item8)
session.commit()

category6 = Category(name='Rock Climbing')
session.add(category6)
session.commit()

category7 = Category(name='Foosball')
session.add(category7)
session.commit()

category8 = Category(name='Skating')
session.add(category8)
session.commit()

category9 = Category(name='Hockey')
session.add(category9)
session.commit()

item9 = Item(name='Stick', description='Description9',
			date_time=randomTime(), category=category9, user=user1)
session.add(item9)
session.commit()

print "Added items!"


