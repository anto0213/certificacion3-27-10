from flask import Flask  

from .config.mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = "voluntame_secreto_2026"

mysql = MySQLConnection(app).mysql

from .controllers import usuarios, misiones, voluntarios