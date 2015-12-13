from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))
		

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=True)

	@property
	def serialize(self):
		'''Return object data in serializeable format'''
		return {
			'name' : self.name,
			'id'   : self.id,
		}
	

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(1000))
	date_time = Column(DateTime(timezone=False))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	picture = Column(String(250))

	@property
	def serialize(self):
		'''Return object data in serializeable format'''
		return {
			'id'			:self.id,
			'title'			:self.name,
			'description' 	:self.description,
			'category_id'	:self.category_id,
		}
	

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.create_all(engine)