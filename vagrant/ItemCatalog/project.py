from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item


app = Flask(__name__)

engine = create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# https://teach.mozilla.org/activities/
# Show all categories and latest items
@app.route('/')
@app.route('/Category')
def showCategories():
	categories = session.query(Category).order_by(asc(Category.name)).all()
	items = session.query(Item).order_by(desc(Item.date_time)).limit(9)
	return render_template('categories.html', categories=categories,
							items=items)

# Show all the items of one category
@app.route('/category/<path:category_name>/')
@app.route('/category/<path:category_name>/items/')
def showCategoryItems():
	items = session.query(Item).order_by(desc(Item.date_time))
	

# @app.route('/category/<path:category_name>/<path:item_name>')
# def showItemDetail():
# 	category = session.query(Category).filter_by(name=category_name).one()
# 	items = session.query(Item).filter_by(category_id=category.id, 
# 											name=item_name).all()

# @app.route('/')



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)