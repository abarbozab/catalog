from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import func
import bleach
from functools import wraps

app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
  'web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            login_session['lasturl'] = url_for('addItem')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login')
def showLogin():
    """
    Render the login template of the application
    """
    state = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in xrange(32)
              )
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/')
def showCatalog():
    """
    Render the categories template and put categories
    and lastest items
    """
    categories = getCategories()
    items = session.query(Item).order_by(desc(Item.create_date)).limit(5).all()
    return render_template(
            'categories.html',
            categories=categories,
            items=items
          )


@app.route('/catalog/<string:category_name>/items')
def showCategoryItems(category_name):
    """
    Render the category template for an specific category_name
    Arg:
    category_name: name of the Category
    """
    categories = getCategories()
    items = session.query(Item).join(Category).filter_by(name=category_name).\
        order_by(desc(Item.create_date)).all()
    return render_template(
            'category.html',
            categories=categories,
            items=items,
            category_name=category_name
          )


@app.route('/catalog/<string:category_name>/<string:item_title>')
def showItem(category_name, item_title):
    """
    Render the item template for an specific category_name and item_title
    Arg:
    category_name: name of the Category
    item_title: title of the Title
    """
    item = session.query(Item).filter_by(title=item_title).join(Category).\
        filter_by(name=category_name).one()
    creator = 0
    if 'username' in login_session:
        if item.user_id == login_session['user_id']:
            creator = login_session['user_id']
    return render_template('item.html', item=item, creator=creator)


@app.route('/catalog/additem', methods=['GET', 'POST'])
@login_required
def addItem():
    """
    Render and process the adition of new item catalog
    Arg:
    category: the name of the Category
    title: the title of the Item
    description: the description of the Item Catalog
    """
    if request.method == 'POST':
        category = session.query(Category).\
            filter_by(name=request.form['category']).one()
        title = bleach.clean(request.form['title'])
        if session.query(Item).filter_by(title=title).count() == 0:
            description = bleach.clean(request.form['description'])
            newItem = Item(
                        user_id=login_session['user_id'],
                        category=category,
                        title=title,
                        description=description
                      )
            session.add(newItem)
            session.commit()
            flash('New Item %s Succesfully Created' % (newItem.title))
        else:
            flash('''Item %s Not Created because already exist other
                Item with the same Title''' % (title))
        return redirect(
                    url_for('showCategoryItems', category_name=category.name))
    else:
        categories = session.query(Category).order_by(asc(Category.name)).all()
        return render_template('additem.html', categories=categories)


@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_title):
    """
    Render and process the edition of new item catalog
    Arg:
    item_title:  the title of the Item to edit
    category: the name of the Category
    title: the title of the Item
    description: the description of the Item Catalog
    """
    edititem = session.query(Item).filter_by(title=item_title).one()
    if edititem.user_id != login_session['user_id']:
        return '''<script>function myFunction()
                {alert("You are not"
              +"authorized to edite this Item. Please create your own"
              +"Item in order to edit.");}
              </script><body onload="myFunction()">'''
    if request.method == 'POST':
        title = bleach.clean(request.form['title'])
        category = session.query(Category).\
            filter_by(name=request.form['category']).one()
        description = bleach.clean(request.form['description'])
        if title == item_title:
            edititem = session.query(Item).filter_by(title=title).one()
            edititem.category = category
            edititem.description = description
            session.add(edititem)
            session.commit()
            flash('Item Successfully Edited')
        else:
            if session.query(Item).filter_by(title=title).count() == 0:
                edititem = session.query(Item).\
                    filter_by(title=item_title).one()
                edititem.title = title
                edititem.category = category
                edititem.description = description
                session.add(edititem)
                session.commit()
                flash('Item Successfully Edited')
            else:
                flash('''Item Can\'t  be Edited because already exist
                    another item with the same Title''')
        return redirect(
            url_for('showCategoryItems', category_name=category.name))
    else:
        categories = session.query(Category).order_by(asc(Category.name)).all()
        return render_template(
            'edititem.html', categories=categories, item=edititem)


@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_title):
    """
    Render and process the deletion of new item catalog
    Arg:
    item_title:  the title of the Item to edit
    """
    deleteitem = session.query(Item).filter_by(title=item_title).one()
    if deleteitem.user_id != login_session['user_id']:
        return '''<script>function myFunction()
                  {alert("You are not authorized to delete"
                  +"this Item. Please create your own Item in order"
                  +"to delete.");}
                  </script><body onload="myFunction()">'''
    if request.method == 'POST':
        deleteitem = session.query(Item).\
            filter_by(title=request.form['item_title']).one()
        category_name = deleteitem.category.name
        session.delete(deleteitem)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(
            url_for('showCategoryItems', category_name=category_name))
    else:
        return render_template('deleteitem.html', item_title=item_title)


@app.route('/catalog.json')
def showJsonCatalog():
    """JSON endpoint that serves the same information
      as displayed in the HTML endpoints
    """
    categories = session.query(Category).all()
    catalog = []
    for c in categories:
        catalog.append(c.serialize)
        items = session.query(Item).filter_by(category_id=c.id).all()
        if len(items) > 0:
            catalog[-1]['item'] = [i.serialize for i in items]
    return jsonify(Category=catalog)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Handle google third-party authentication & authorization service
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
              json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('''https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s''' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(
              json.dumps('Failed to upgrade the authorization code'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
              json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
              json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
              json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return "done!"


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Handle facebook third-party authentication & authorization service
    """
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
    url = '''https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s''' % (
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

    """ The token must be stored in the login_session in order to properly logout,
    let's strip out the information before the equals sign in our token """
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = '''https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s" % login_session['username'])
    return 'Done'


@app.route('/disconnect')
def disconnect():
    """
    Disconnect of application
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


@app.route('/gdisconnect')
def gdisconnect():
    """
    Handle google disconnect
    """
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
              json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
              json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
              json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbdisconnect')
def fbdisconnect():
    """
    Handle facebook disconnect
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = '''https://graph.facebook.com/%s/permissions?access_token=%s''' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    return "you have been logged out"


def getUserID(email):
    """
    Get user Id by email
    Args:
      email:  the email of the user
    Returns:
    the id number of the user
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def createUser(login_session):
    """
    Create a user
    Args:
      login_session:  the login_session of the app
    Returns:
    the id number of the user
    """
    newUser = User(
                name=login_session['username'],
                email=login_session['email'],
                picture=login_session['picture']
              )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getCategories():
    """
    Get categories of the application
    Returns:
    the list of tubles of categories and number of items
    """
    categories = session.query(Category, func.count(Item.id)).outerjoin(Item).\
        group_by(Category.id).order_by(asc(Category.name)).all()
    return categories

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
