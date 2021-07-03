from flask.views import MethodView
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
# from config import KEY_TOKEN_AUTH
import datetime
import time
import bcrypt
import jwt
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ieas_db'

mysql = MySQL(app)

class registrousercontrollers(MethodView):
   
    def post(self):
        # simulacion de espera en el back con 1.5 segundos
        time.sleep(1)
        content = request.get_json()
        nombre = content.get("nombre")
        apellidos = content.get("apellidos")
        correo = content.get("correo")
        contraseña = content.get("contraseña")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(contraseña), encoding= 'utf-8'), salt)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registrousuario(nombre, apellidos,correo, contraseña) VALUES (%s,%s,%s,%s)",
                    (nombre, apellidos, correo, hash_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"registro ok": True, "nombre": nombre,"apellidos": apellidos, "correo": correo}), 200
       

class LoginUserControllers(MethodView):
    """
        Login
    """

    def post(self):
        time.sleep(.500)
        content = request.get_json()
        email = content.get("correo")
        password = content.get("contraseña")
        # creamos comandos sql para verificar que la informacion que ingresamos sea correcta
        curl = mysql.connection.cursor()
        curl.execute(
            "SELECT id_user, nombre, apellidos, correo, contrasena FROM usuario WHERE correo=%s", ([email]))
        user = curl.fetchall()
        user = user[0]
        id_user = user[0]
        correo = user[3]
        clave = user[4]
        usuario = {}
        usuario[correo] = {"contraseña": clave}
        curl.close()
        # creamos diversos caminos que el sofware puede coger
        if len(user) > 0:

            passwordb = usuario[correo]["contraseña"]

            if bcrypt.checkpw(bytes(str(password), encoding='utf-8'), passwordb.encode('utf-8')):

                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=10), 'correo': correo, 'id_user': id_user, 'tipo_user': 'usuario'}, KEY_TOKEN_AUTH, algorithm='HS256')

                return jsonify({"auth": True, "nombre": user[1], "apellidos": user[2], "correo": user[3], "token": encoded_jwt}), 200

        else:
            return jsonify({"auth": False, }), 403
