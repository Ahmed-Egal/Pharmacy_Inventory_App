from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow 
from marshmallow import Schema, fields 


app = Flask(__name__)


#initialize db and connectio
# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres: @localhost/pharmacy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)



# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app,db)
ma = Marshmallow(app)


#define models
class Categories(db.Model):
    categories_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(60), nullable=False)

    def to_dict(self):
        return {
            "categories_id": self.categories_id,
            "category_name": self.category_name,
    }



class Products(db.Model):
    products_id = db.Column(db.Integer, primary_key=True)
    products_name = db.Column(db.String(60), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price=db.Column(db.Integer, nullable=False)
    expiry=db.Column(db.Date, nullable=False)

    # add fk
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.categories_id'))

    def to_dict(self):
        return {
            "products_id": self.products_id,
            "products_name": self.products_name,
            "quantity": self.quantity,
            "price": self.price,
            "expiry": self.expiry.isoformat() if self.expiry else None,
            "categories_id": self.categories_id
    }


class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False)


# marshmallow schema

# class SuppliersSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name','contact', 'email')



# supplier_schema = SuppliersSchema()
# suppliers_schema = SuppliersSchema(many=True)

# @app.route('/suppliers', methods=['GET'])
# def get_suppliers():
#     all_suppliers = Suppliers.query.all()
#     return suppliers_schema.dump(all_suppliers)

    




@app.route('/')
def home():
    return 'Hello there, Welcome to Flask!'


@app.route('/<name>')
def hello(name):
    return f'Hello there, Welcome to the {name} server!'



@app.route('/products', methods=['GET'])
def products():
    products = Products.query.all()
    return jsonify([product.to_dict() for product in products]) 


@app.route('/categories', methods=['GET'])
def categories():
    categories=Categories.query.all()
    return jsonify([category.to_dict() for category in categories])


@app.route('/products/<int:id>', methods=['GET'])
def product_byID(id):
    product = Products.query.get(id)

    
    return jsonify(product.to_dict())
    
    
 

# in this request, we check if the entry is there. is the date, name, quantity in the posted data. Next check the entered data if it has the correct type, length etc
@app.route('/products',methods=['POST'])
def add_product():
    data = request.get_json()

    if 'products_name' not in data:
        return 'Product name is missing!'
    elif not isinstance(data['products_name'], str):
        return 'Product name must be a string.'
    elif len(data['products_name']) > 60:
        return 'Product name is too long'
    


    if 'quantity' not in data:
        return 'Quantity is missing!'
    elif not isinstance(data['quantity'], int):
        return 'Quantity must be a number.'
    elif not (0 < data['quantity'] <= 500) :
        return 'Quantity has to be between 1 and 500'
    

    if 'price' not in data:
        return 'Price is missing!'
    elif not isinstance(data['price'], int):
        return 'Price must be a number.'
    

    if 'expiry' not in data:
        return 'Expiry date is missing!'
    try:
        expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
    except ValueError:
        return 'Expiry must be in YYYY-MM-DD format.'
    



    new_product= Products(
        products_name=data['products_name'],
        quantity=data['quantity'],
        price=data['price'],
        expiry=expiry_date,
    )


    db.session.add(new_product)
    db.session.commit()


    return {'msg' : 'Product added successfully'}, 201


@app.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    product = Products.query.get(id)
    
    if not product:
        return 'Product not found', 404
    
    data = request.get_json()

    if 'products_name' in data:
        product.products_name = data['products_name']
    
    if 'quantity' in data:
        product.quantity = data['quantity']

    if 'price' in data:
        product.price = data['price']

    if 'expiry' in data:
        try:
            product.expiry = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
        except ValueError:
            return 'Invalid expiry date format', 400

    db.session.commit()

    return 'Product updated successfully'



@app.route('/products/<int:id>', methods=['PUT'])
def updating_full_product(id):
    existing_product = Products.query.get(id)

    data = request.get_json()

    if not existing_product:
        return 'Product not found', 404
    
    if 'products_name' not in data:
        return "Product name is missing !"
    elif not isinstance(data['products_name'], str):
        return "Product name must be a string."
    elif len(data['products_name']) > 60 :
        return "Product name must not exceed 60 characters."
    

    if 'quantity' not in data:
        return "Quantity is missing!"
    elif not isinstance(data['quantity'], int):
        return "Quantity must be an integer"
    elif not  (0 < data['quantity'] <= 500):
        return "Quantity has to be between 0 and 500"
    

    if 'price' not in data:
        return "Price not included"
    elif not isinstance(data['price'], int):
        return "Price must be a number"
    

    if 'expiry' not in data:
        return "No expiry date included."
    try:
        expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
    except ValueError : 
        return "Date must be in YYYY-MM-DD format"
    


    existing_product.products_name=data['products_name']
    existing_product.quantity=data['quantity']
    existing_product.price=data['price']
    existing_product.expiry=expiry_date



    db.session.commit()

    return {'msg' : 'Product updated successfully'}, 200



@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    deleting_product = Products.query.get(id)

    if not deleting_product:
        return "Product not found", 404
    
    else:
        db.session.delete(deleting_product)
        db.session.commit()

    return "Product successfully deleted", 200
    
    


        
    























if __name__ == "__main__":
    app.run(debug=True)


# C:\Program Files\PostgreSQL\15\ssl\certs\ca-bundle.crt