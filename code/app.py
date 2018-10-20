from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
  def get(self, name):
    for item in items:
      if item['name'] == name:
        return item
    return { 'item': None }, 404
  
  def post(self, name):
    item = { 'name': name, 'price': 12.00 }
    if len([i for i in items if i['name'] == name]) == 0:
      items.append(item)
      return item, 201
    else:
      return { 'message': 'Item already exits'}, 403


api.add_resource(Item, '/item/<string:name>') # make the Item resource accessible from the api at the route provided as the second argument

app.run(port=5000, debug=True)


