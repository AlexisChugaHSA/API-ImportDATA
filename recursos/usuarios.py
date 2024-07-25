from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UsuarioSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from passlib.hash import pbkdf2_sha256
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, abort, render_template, request, redirect, jsonify
blp = Blueprint("Usuarios", "usuarios", description="Operations on users")


@blp.route("/usuarios")
class Usuarios(MethodView):
    @blp.response(200, UsuarioSchema(many=True))
    @jwt_required()
    def get(self):
        usuarios = []
        cursor = obtener_conexion().cursor()
        cursor.execute("Select id_usuario,usuario,password from usuario")
        result = cursor.fetchall()
        cursor.close()
        for fila in result:
            usuario = {'id_usuario': fila[0],
                       'usuario': fila[1], 'password': fila[2]}
            usuarios.append(usuario)
        return usuarios


@blp.route("/usuario")
class Usuario(MethodView):
    @blp.arguments(UsuarioSchema)
    #@jwt_required()
    def post(self, user_data):
        conexion = obtener_conexion()
        password = pbkdf2_sha256.hash(user_data['password']),
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into usuario(usuario,password)
                        values('{0}','{1}')""".format(user_data['usuario'], password[0]))
                conexion.commit()
        with conexion.cursor() as cursor2:
                cursor2.execute(
                    """SELECT * from usuario order by ID_usuario desc limit 1 """)
                datos = cursor2.fetchone()
                usuario = {
                    'id_usuario': datos[0], 'usuario': datos[1]}
                return usuario, 200


@blp.route("/usuario/<int:id>")
class User(MethodView):
    @blp.response(200, UsuarioSchema)
    #@jwt_required()
    def get(self, id):
        cursor = obtener_conexion().cursor()
        cursor.execute(
            "Select id_usuario, usuario,token from usuario where id_usuario={0}".format(id))
        datos = cursor.fetchone()
        cursor.close()
        if datos != None:
            usuario = {'id_usuario': datos[0], 'usuario': datos[1],'token': datos[2]}
            return usuario, 200
        else:
            return {"Mensaje": "Usuario no encontrado"}, 409
        
    @blp.arguments(UsuarioSchema)
    @jwt_required()
    def put(self, user_data, id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "Select * from usuario where id_usuario='{0}'".format(id))
        datos = cursor.fetchone()
        # print(datos)
        if datos != None:
            password = pbkdf2_sha256.hash(user_data['password']),
            cursor.execute("Update usuario set password='{0}' where id_usuario={1}".format(
                 password[0], id))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Usuario actualizado"}, 200
        else:
            return {"Mensaje": "Usuario no encontrado"}, 409

@blp.route("/usuario/<string:nombre>")
class User(MethodView):
    @blp.response(200, UsuarioSchema)
    #@jwt_required()
    def get(self, nombre):
        cursor = obtener_conexion().cursor()
        print(nombre)
        cursor.execute(
            "Select id_usuario,usuario,token from usuario where usuario='{0}'".format(nombre))
        datos = cursor.fetchone()
        cursor.close()
        if datos != None:
            usuario = {'id_usuario': datos[0], 'usuario': datos[1],'token': datos[2]}
            return usuario, 200
        else:
            return {"Mensaje": "Usuario no encontrado"}, 409



    @jwt_required()
    def delete(self, id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("Delete from usuario where id_usuario={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Usuario eliminado"}, 200

@blp.route("/reset_password/<string:nombre>")
class User(MethodView):
    @jwt_required()
    def put(self, nombre):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "Select * from usuario where usuario='{0}'".format(nombre))
        datos = cursor.fetchone()
        print(datos)
        if datos != None:
            passwordTemp=generar_contrasena_aleatoria()
            print(passwordTemp)
            password = pbkdf2_sha256.hash(passwordTemp),
            cursor.execute("Update usuario set usuario='{0}', password='{1}' where usuario='{0}'".format(
                nombre, password[0]))
            conexion.commit()
            conexion.close()
            #enviar_correo_electronico(datos[1],"Cambio de contrasena",password)
            return {"Mensaje": "Contrasena reseteada"}, 200
        else:
            return {"Mensaje": "Usuario no encontrado"}, 409

@blp.route("/comprobar_password")
class User(MethodView):
    @blp.arguments(UsuarioSchema)
    #@jwt_required()
    def post(self, user_data):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "Select * from usuario where id_usuario='{0}'".format(user_data['id_usuario']))
        datos = cursor.fetchone()
        print(datos)
        if datos != None and pbkdf2_sha256.verify(user_data["password"], datos[2]):
            password = pbkdf2_sha256.hash(user_data['password'])
            return {"mensaje": "OK"}, 200
        else:
            return {"mensaje": "NO"}
@jwt_required()
def generar_contrasena_aleatoria(longitud=8):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for i in range(longitud))
    return contrasena


@blp.route("/comprobar-usuario/<string:nombre>")
class User(MethodView):
    def get(self, nombre):
        cursor = obtener_conexion().cursor()
        print(nombre)
        cursor.execute(
            "Select id_usuario,usuario,token from usuario where usuario='{0}'".format(nombre))
        datos = cursor.fetchone()
        cursor.close()
        if datos != None:
            usuario = {'id_usuario': datos[0], "Mensaje": "SI"}
            return usuario, 200
        else:
            return {"Mensaje": "NOEN"}, 409