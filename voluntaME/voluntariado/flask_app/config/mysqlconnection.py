from flask_mysqldb import MySQL

class MySQLConnection:
    def __init__(self, app):
        app.config["MYSQL_HOST"] = "localhost"
        app.config["MYSQL_USER"] = "root"
        app.config["MYSQL_PASSWORD"] = ""
        app.config["MYSQL_DB"] = "voluntame_db"
        app.config["MYSQL_CURSORCLASS"] = "DictCursor"
        self.mysql = MySQL(app)