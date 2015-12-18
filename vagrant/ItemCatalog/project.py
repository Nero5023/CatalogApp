from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
from datetime import datetime
import random
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests, string
import xml.dom.minidom as minidom
import codecs
import os
from werkzeug import secure_filename
from flask import send_from_directory

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','git'])


engine = create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# Show all categories and latest items
@app.route('/')
@app.route('/category')
def showCategories():
	categories = session.query(Category).order_by(asc(Category.name)).all()
	items = session.query(Item).order_by(desc(Item.date_time)).limit(9)
	if login_session.get('user_id') is None:
		return render_template('publiccategories.html', categories=categories,
							items=items)
	else:
		return render_template('categories.html', categories=categories,
							items=items)

# Oauth login
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

# Oauth disconnect
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        print "success log out"
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))



@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(data['email'])
    if user_id == None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You have been logged out"

# user help method
def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'],
				picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

# Show all the items of one category
@app.route('/category/<path:category_name>/')
@app.route('/category/<path:category_name>/items/')
def showCategoryItems(category_name):
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category_id=category.id)
	categories = session.query(Category).order_by(asc(Category.name)).all()
	if login_session.get('user_id') is None:
		return render_template('publicitems.html', categories=categories, 
			category_name=category_name, items=items)
	else:
		return render_template('items.html', categories=categories, 
			category_name=category_name, items=items)


# Show item detials
@app.route('/category/<path:category_name>/<path:item_name>/')
def showItemDetail(category_name,item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	item = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).one()
	if login_session.get('user_id') is not None and login_session['user_id'] == item.user_id:
		return render_template('itemdetail.html', item=item)
	else:
		print 'public'
		return render_template('publicitemdetail.html', item=item)

# Check item in category if is already exist
@app.route('/check/<path:category_name>/<path:item_name>/')
def checkIfAlreadyExist(category_name,item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).all()
	if len(items) == 0:
		return jsonify(isExist=False)
	else:
		return jsonify(isExist=True)

# Edit item
@app.route('/category/<path:category_name>/<path:item_name>/edit/', methods=['GET','POST'])
def editItem(category_name, item_name):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Category).filter_by(name=category_name).one()
	editItem = session.query(Item).filter_by(category_id=category.id, 
											name=item_name).one()
	if editItem.user_id != login_session['user_id']:
		return alertScript('edit', 'item')
	if request.method == 'POST':
		if request.form['name']:
			editItem.name = request.form['name']
		if request.form['description']:
			editItem.description = request.form['description']
		if request.form['category']:
			newCategory = session.query(Category).filter_by(
							name=request.form['category']).one()
			editItem.category = newCategory
		if request.files['file']:
			file_path = uploadFile()
			editItem.picture = file_path

		session.add(editItem)
		session.commit()
		flash('Item Successfully Edited')
		return redirect(url_for('showItemDetail', 
				category_name=editItem.category.name,item_name=editItem.name))
	else:
		categories = session.query(Category).order_by(asc(Category.name)).all()
		return render_template('editornewitem.html', categories=categories, 
			item=editItem,category_name=category_name, isEdit=True)

# New item
@app.route('/newitem/', methods=['GET','POST'])
def newItem():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		# error message
		category = session.query(Category).filter_by(
						name=request.form['category']).one()
		time = datetime.now()
		user = session.query(User).filter_by(id=login_session['user_id']).one()
		file_path = uploadFile() 
		newItem = Item(name=request.form['name'], date_time=time,
				description=request.form['description'], category=category,
				user=user, picture=file_path)
		session.add(newItem)
		flash("%s Successfully Added" % newItem.name)
		session.commit()
		return redirect(url_for('showCategories'))
	else:
		categories = session.query(Category).order_by(asc(Category.name)).all()
		return render_template('editornewitem.html', categories=categories,
							isEdit=False)


def alertScript(method, name):
    return "<script>function alertFunc() {alert('You are not authorized to %s \
        this %s. Please create your own %s in order to %s.');}\
        </script><body onload='alertFunc()'>" % (method, name, name, method)

# upload file help methond
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def uploadFile():
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path = url_for('uploaded_file',filename=filename)
			# check in database if have the same name of the picture
			if session.query(Item).filter_by(picture=path).all() != []:
				filename = '0' + filename
				path = url_for('uploaded_file',filename=filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print url_for('uploaded_file',filename=filename)
			return url_for('uploaded_file',filename=filename)
		return None

@app.route('/upload/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/categorybd/<filename>')
def categorybd(filename):
	return send_from_directory('static/categorybd',filename)

# delete item 
# use token for prevent CSRF
@app.route('/category/<path:category_name>/<path:item_name>/delete/', methods=['GET','POST'])
def deleteItem(category_name,item_name):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Category).filter_by(name=category_name).one()
	# maybe some problem
	itemToDelete = session.query(Item).filter_by(category_id=category.id, 
										name=item_name).one()
	if itemToDelete.user_id != login_session['user_id']:
		return alertScript('delete', 'item')
	if request.method == 'POST':
		token = request.cookies.get('cookie_token')
		if request.form['cookie_token'] == token:
			session.delete(itemToDelete)
			session.commit()
			print 'success'
			flash('%s Successfully delete' % itemToDelete.name)
			return redirect(url_for('showCategories'))
		else:
			response = make_response(json.dumps('Invalid token parameter.'), 401)
        	response.headers['Content-Type'] = 'application/json'
        	return response
	else:
		token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
		resp = make_response(render_template('deleteitem.html',
					category_name=category_name,item_name=item_name, cookie_token=token))
		resp.set_cookie('cookie_token', token)
		return resp

# help method for categoriesJSON
# make categories info into a dic 
def getCategoiresDic():
	categories = session.query(Category).order_by(asc(Category.name)).all()
	categoriesDic = []
	for category in categories:
		items = session.query(Item).filter_by(category_id=category.id).all()
		dic = category.serialize
		dic['Item'] = [item.serialize for item in items]
		categoriesDic.append(dic)

# return categories json info
@app.route('/catalog.json')
def categoriesJSON():
	categories = session.query(Category).order_by(asc(Category.name)).all()
	jsonlist = []
	for category in categories:
		items = session.query(Item).filter_by(category_id=category.id).all()
		dic = category.serialize
		dic['Item'] = [item.serialize for item in items]
		jsonlist.append(dic)

	print jsonlist
	return jsonify(category=jsonlist)

# return categories xml json
@app.route('/catalog.xml')
def categoriesXML():
	categories = session.query(Category).order_by(asc(Category.name)).all()
	xmlList = []
	for category in categories:
		items = session.query(Item).filter_by(category_id=category.id).all()
		dic = category.serialize
		dic['Item'] = [item.serialize for item in items]
		xmlList.append(dic)


	impl = minidom.getDOMImplementation()
	dom = impl.createDocument(None, 'catalog', None)
	root = dom.documentElement
	# root = doc.createElement('categories')
	# root = ET.Element('categories')
	
	for categoryDic in xmlList:
		category = dom.createElement('category')

		category_name = dom.createElement('name')
		category_name_text = dom.createTextNode(categoryDic['name'])
		category_name.appendChild(category_name_text)
		category.appendChild(category_name)

		category_id = dom.createElement('id')
		category_id_text = dom.createTextNode(repr(categoryDic['id']))
		category_id.appendChild(category_id_text)
		category.appendChild(category_id)

		items = dom.createElement('items')

		for itemDic in categoryDic['Item']:
			item = dom.createElement('item')

			item_title = dom.createElement('title')
			item_title_text = dom.createTextNode(itemDic['title'])
			item_title.appendChild(item_title_text)
			item.appendChild(item_title)

			item_id = dom.createElement('id')
			item_id_text = dom.createTextNode(repr(itemDic['id']))
			item_id.appendChild(item_id_text)
			item.appendChild(item_id)

			item_description = dom.createElement('description')
			item_description_text = dom.createElement(itemDic['description'])
			item_description.appendChild(item_description_text)
			item.appendChild(item_description)

			item_category_id = dom.createElement('category_id')
			item_category_id_text = dom.createTextNode(repr(itemDic['category_id']))
			item_category_id.appendChild(item_category_id_text)
			item.appendChild(item_category_id)

			items.appendChild(item)

		category.appendChild(items)
		root.appendChild(category)


	print dom.toprettyxml()
	return dom.toprettyxml()


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.debug = True
	app.run(host='0.0.0.0', port=8000)