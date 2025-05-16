# import certifi
# print(certifi.where())



# unset SSL_CERT_FILE
# export SSL_CERT_FILE="/c/Python312/Lib/site-packages/certifi/cacert.pem"
# python -m pip install flask sqlalchemy
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# db = SQLAlchemy(app)

# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

# with app.app_context():
#     db.create_all()
#     print("Flask and SQLAlchemy are working!")
