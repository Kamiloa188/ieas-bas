from collections import UserDict
from flask import Flask
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from routes import *
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ieas_db'

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "*"}})


app.add_url_rule(user["registro_user"], view_func=user["registro_user_controllers"])