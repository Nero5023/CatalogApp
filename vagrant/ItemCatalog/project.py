from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from datetime import datetime

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
def showCategoryItems(category_name):
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category_id=category.id)
	categories = session.query(Category).order_by(asc(Category.name)).all()
	return render_template('items.html', categories=categories, 
			category_name=category_name, items=items)


@app.route('/category/<path:category_name>/<path:item_name>/')
def showItemDetail(category_name,item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	item = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).one()
	return render_template('itemdetail.html', item=item)


@app.route('/category/<path:category_name>/<path:item_name>/edit/', methods=['GET','POST'])
def editItem(category_name, item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	editItem = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).one()
	if request.method == 'POST':
		if request.form['name']:
			editItem.name = request.form['name']
		if request.form['description']:
			editItem.description = request.form['description']
		if request.form['category']:
			newCategory = session.query(Category).filter_by(
							name=request.form['category']).one()
			editItem.category = newCategory
		session.add(editItem)
		session.commit()
		flash('Item Successfully Edited')
		return redirect(url_for('showItemDetail', 
				category_name=editItem.category.name,item_name=editItem.name))
	else:
		categories = session.query(Category).order_by(asc(Category.name)).all()
		return render_template('editornewitem.html', categories=categories, 
			item=editItem,category_name=category_name, isEdit=True)

@app.route('/newitem/', methods=['GET','POST'])
def newItem():
	if request.method == 'POST':
		# error message
		category = session.query(Category).filter_by(
						name=request.form['category']).one()
		time = datetime.now()
		newItem = Item(name=request.form['name'], date_time=time,
				description=request.form['description'], category=category)
		session.add(newItem)
		session.commit()
		flash("%s Successfully Added" % newitem.name)
		return redirect(url_for('showCategories'))
	else:
		categories = session.query(Category).order_by(asc(Category.name)).all()
		return render_template('editornewitem.html', categories=categories,
							isEdit=False)

@app.route('/category/<path:category_name>/<path:item_name>/delete/', methods=['GET','POST'])
def deleteItem(category_name,item_name):
	if request.method == 'POST':
		category = session.query(Category).filter_by(name=category_name).one()
		itemToDelete = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).one()
		session.delete(itemToDelete)
		session.commit()
		print 'success'
		flash('%s Successfully delete' % itemToDelete.name)
		return redirect(url_for('showCategories'))
	else:
		return render_template('deleteitem.html',
					category_name=category_name,item_name=item_name)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)