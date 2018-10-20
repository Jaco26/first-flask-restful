from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
api = Api(app)

#   JWT creates a new endpoint ('/auth')
# When we call /auth, we send a username and password.
# the JWT extension passes that data to the 'authenticate'
# method we imported from our module 'security.py'
# If username and password are legit, /auth returns a JWT which reprensents
# a user's identity
#   We can send that JWT back to a user and when they send further requests
# to other endpoints, JWT uses the 'identity' method imported from 'security.py'
# to get that user's information.
jwt = JWT(app, authenticate, identity)

items = [
  {
    'name': 'Water Bottle',
    'price': 9.00
  },
  {
    'name': 'Plate',
    'price': 7.00
  },
]

class Item(Resource): # all resources will be classes which inherit from flask_restful.Resource
  @jwt_required()
  def get(self, name):
    # next(filter()) returns the first item found by filter. 
    # if the filter doesn't find any items, calling next on it will throw an error
    # it's a good idea to provide a default value of None for next() to return
    item = next(filter(lambda x: x['name'] == name, items), None) 
    return { 'item': item }, 200 if item else 404
  
  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None):
      return { 'message': 'An item with name {} already exists'.format(name)}, 400
    # force=True - request doesn't need Content-Type header
    # silent=True - if Content-Type is not application/json, no error is thrown, just return None
    data = request.get_json() 
    item = { 'name': name, 'price': data['price'] }
    items.append(item)
    return item, 201


  def put(self, name):
    pass

class ItemList(Resource):
  def get(self):
    return { 'items': items }


api.add_resource(Item, '/item/<string:name>') # make the Item resource accessible from the api at the route provided as the second argument
api.add_resource(ItemList, '/items')

@app.route('/')
def index():
  return render_template('index.html')

app.run(port=5000, debug=True)


