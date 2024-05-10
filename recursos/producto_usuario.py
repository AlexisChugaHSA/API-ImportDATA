from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ProductoUsuarioSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from flask import Flask, abort, render_template, request, redirect, jsonify
blp = Blueprint("Producto_Usuario", "producto_usuario",
                description="Operaciones con producto_usuario")


@blp.route("/producto-usuarios")
class ProdUsersSchema(MethodView):
    @blp.response(200, ProductoUsuarioSchema(many=True))
    @jwt_required()
    def get(self):
        p_us = []
        cursor = obtener_conexion().cursor()
        cursor.execute(
            "Select id_producto_usuario,id_usuario,id_producto,activo, precio, fecha from producto_usuario")
        result = cursor.fetchall()
        cursor.close()
        for fila in result:
            p_u = {'id_producto_usuario': fila[0], 'id_usuario': fila[1],
                'id_producto': fila[2], 'activo': fila[3], 'precio': fila[4], 'fecha': fila[5], 'periodo': fila[6], 'fecha_hasta': fila[7]}
            p_us.append(p_u)
        return p_us


@blp.route("/producto-usuario")
class ProductoUsuario(MethodView):
    @blp.arguments(ProductoUsuarioSchema)
    @jwt_required()
    def post(self, user_data):
        fecha_actual = datetime.now()
        fecha_hasta = fecha_actual + timedelta(days=user_data['periodo']*30)
        fecha_hastaf= fecha_hasta.strftime('%Y-%m-%d')
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""Insert into producto_usuario(id_usuario,id_producto,id_pago,activo,precio,fecha,periodo,fecha_hasta)
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format(user_data['id_usuario'], user_data['id_producto'],user_data['id_pago'], user_data['activo'], user_data['precio'], fecha_actual, user_data['periodo'],fecha_hastaf))
        conexion.commit()
        with conexion.cursor() as cursor:
            cursor.execute(
                """SELECT * from producto_usuario where id_usuario='{0}' and id_producto='{1}' and id_pago='{2}' and activo='{3}' and precio='{4}' and fecha='{5}' and periodo='{6}' and fecha_hasta='{7}'"""
                .format(user_data['id_usuario'], user_data['id_producto'],user_data['id_pago'], user_data['activo'], user_data['precio'], fecha_actual, user_data['periodo'],fecha_hastaf))
        datos = cursor.fetchone()
        prod_user = {'id_producto_usuario': datos[0], 'id_usuario': datos[1],
            'id_producto': datos[2], 'id_pago': datos[3], 'activo': datos[4], 'precio': datos[5], 'fecha': datos[6],'periodo': datos[7], 'fecha_hasta': datos[8]}
        return prod_user
    
    @blp.arguments(ProductoUsuarioSchema)      
    @jwt_required() 
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from producto_usuario where id_producto_usuario='{0}'".format(user_data['id_producto_usuario']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update producto_usuario set id_usuario='{0}', id_producto='{1}', activo='{2}', precio='{3}', fecha='{4}' where id_prod_user={5}".
                           format(user_data['id_usuario'],user_data['id_producto'],user_data['activo'],user_data['precio'],user_data['fecha'],user_data['id_log_prod_user']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Producto-Usuario actualizado"},200
        else:
            return {"Mensaje": "Producto-Usuario no encontrado"},409
            
@blp.route("/producto-usuario/<int:id>")
class User(MethodView):
    @blp.response(200, ProductoUsuarioSchema(many=True))
    @jwt_required()
    def get(self, id):
        p_us = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM producto_usuario WHERE id_usuario = %s AND activo = 1 ORDER BY id_producto, fecha_hasta DESC", (id,))
        result = cursor.fetchall()

        # Utilizamos un diccionario para rastrear los productos por su id_producto
        productos_por_id = {}
        for fila in result:
            id_producto = fila[2]
            # Si el producto ya existe en el diccionario y la fecha_hasta es mayor, lo actualizamos
            if id_producto in productos_por_id:
                if fila[8] > productos_por_id[id_producto][8]:
                    productos_por_id[id_producto] = fila
            else:
                productos_por_id[id_producto] = fila

        # Ahora, agregamos los productos únicos al resultado final
        for fila in productos_por_id.values():
            p_u = {
                'id_producto_usuario': fila[0],
                'id_usuario': fila[1],
                'id_producto': fila[2],
                'id_pago': fila[3],
                'activo': fila[4],
                'precio': fila[5],
                'fecha': fila[6],
                'periodo': fila[7],
                'fecha_hasta': fila[8]
            }
            p_us.append(p_u)
        
        return p_us
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from prodcto_usuario where id_producto_usuario={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Producto-Usuario eliminada"},200



'''
@blp.route("/producto-usuario/<int:id>")

class User(MethodView):
    @blp.response(200, ProductoUsuarioSchema(many=True))
    @jwt_required()
    def get(self,id):
        p_us = []
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("Select * from producto_usuario where id_usuario={0} and activo=1".format(id))
        result=cursor.fetchall()
        for fila in result:
            p_u = {'id_producto_usuario': fila[0], 'id_usuario': fila[1],
                'id_producto': fila[2],'id_pago': fila[3], 'activo': fila[4], 'precio': fila[5], 'fecha': fila[6], 'periodo': fila[7], 'fecha_hasta': fila[8]}
            p_us.append(p_u)
        return p_us
'''



        
@blp.route("/verificacion-prod-user")
class User(MethodView):
    @jwt_required()
    def put(self):
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("Update producto_usuario set activo=0 where activo=1 and fecha_hasta<='{0}'".format(fecha_actual))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Producto-Usuario actualizado"},200
