from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import Config
from routes import registrar_rutas
from flask_jwt_extended import JWTManager

app     = Flask(__name__)
app.config.from_object(Config)
mysql   = MySQL(app)

app.mysql = mysql

jwt = JWTManager(app)

CORS(app,
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

registrar_rutas(app)

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0")