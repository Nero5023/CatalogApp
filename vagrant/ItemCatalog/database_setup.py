from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=True)

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(1000))
	date_time = Column(DateTime(timezone=False))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.create_all(engine)