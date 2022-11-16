from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from werkzeug.utils import secure_filename

application = Flask(__name__)
app = application
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'images'
#allowed_extensions = set(['image/jpeg', 'image/png', 'jpeg'])

#def allowed_file(filename):
#return filetype in allowed_extentions


class Products(db.Model):
  #__tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  image = db.Column(db.String(50), nullable=True)
  data = db.Column(db.LargeBinary, nullable=True)
  name = db.Column(db.String(50))
  price = db.Column(db.Integer)
  description = db.Column(db.String(150))
  size = db.Column(db.String(50))

  def create(self):
    db.session.add(self)
    db.session.commit()

  def __init__(self, name, price, description, size):
    #self.image = image
    self.name = name
    self.price = price
    self.description = description
    self.size = size

  def __repr__(self):
    return '<Product %d>' % self.id


class ProductsSchema(Schema):

  class Meta:
    model = Products

  id = fields.Number(dump_only=True)
  image = fields.String(dump_only=True)
  data = fields.String(dump_only=True)
  name = fields.String(required=True)
  price = fields.Number(required=True)
  description = fields.String(required=True)
  size = fields.String(required=True)


@app.route('/', methods=['GET'])
def index():
  get_products = Products.query.all()
  product_schema = ProductsSchema(many=True)
  products = product_schema.dump(get_products)
  return make_response(jsonify({'products': products}))


@app.route('/', methods=['POST'])
def create_product():
  data = request.get_json()
  product_schema = productsSchema()
  product = product_schema.load(data)
  result = product_schema.dump(products.create()).data
  return make_response(jsonify({'product': product}), 201)


@app.route('/products/<id>', methods=['GET'])
def get_product_by_id(id):
  get_product = Products.query.get(id)
  product_schema = ProductsSchema()
  product = product_schema.dump(get_product)
  return jsonify({'product': product})


@app.route('/products/<id>', methods=['PUT'])
def update_by_id(id):
  data = request.get_json()
  get_product = Products.query.get(id)
  if data.get('name'):
    get_product.name = data['name']
  if data.get('price'):
    get_product.price = data['price']
  if data.get('description'):
    get_product.description = data['description']
  if data.get('size'):
    get_product.size = data['size']
  db.session.add(get_product)
  db.session.commit()
  product_schema = ProductsSchema(
    only=['id', 'name', 'price', 'description', 'size'])
  product = product_schema.dump(get_product)
  return make_response(jsonify({'product': product}))


@app.route('/products/<id>', methods=['DELETE'])
def delete_product_by_id(id):
  get_product = Products.query.get(id)
  db.session.delete(get_product)
  db.session.commit()
  return make_response('', 204)


@app.route('/upload/<id>', methods=['GET', 'POST'])
def upload_image(id):
  if request.method == 'POST':
    file = request.files['file']
    upload = Products(filename=file.filename, data=file.read())
    db.session.add(upload)
    db.session.commit()
    return make_response(jsnofiy(f'{file.filename}'))


if __name__ == '__main__':
  app.run(host="0.0.0.0")