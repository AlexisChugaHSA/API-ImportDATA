from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CUPSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Cupon_Usuario_Pago", "cupon_usuario_pago", description="Operaciones con cupon_usuario_pago")

@blp.route("/cups")
class CategoriaSchema(MethodView):
    @blp.response(200, CUPSchema(many=True))
    @jwt_required()
    def get(self):
        cups=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_cupon_usuario_pago,id_usuario,id_cupon,id_pago,fecha from cupon_usario_pago")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            cup={'id_cupon_usuario_pago':fila[0],'id_usuario':fila[1],'id_cupon':fila[2],'id_pago':fila[3],'fecha':fila[4]}
            cups.append(cup)
        return cups


@blp.route("/cup")
class CUP(MethodView):
    @blp.arguments(CUPSchema)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from cupon_usuario_pago where id_usuario='{0}' and id_cupon='{1}' and id_pago='{2}'".
                       format(user_data['id_usuario'],user_data['id_cupon'],user_data['id_pago']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into cupon_usuario_pago(id_usuario,id_cupon,id_pago,fecha) 
                        values('{0}','{1}','{2}','{3}')""".format(user_data['id_usuario'],user_data['id_cupon'],user_data['id_pago'],user_data['fecha']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"Cupon_Usuario_Pago registrado"},201 
        else:
            return {"mensaje":"Ya existe el CUP que se desea registrar"},409

    @blp.arguments(CUPSchema)  
    @jwt_required()     
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from cupon_usuario_pago where id_cupon_usario_pago='{0}'".format(user_data['id_cupon_usario_pago']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update cupon_usuario_pago set id_usuario='{0}', id_cupon='{1}', id_pago='{2}', fecha='{3}' where id_cupon_usario_pago={4}".
                           format(user_data['id_usuario'],user_data['id_cupon'],user_data['id_pago'],user_data['fecha'],user_data['id_cupon_usario_pago']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "CUP actualizado"},200
        else:
            return {"Mensaje": "CUP no encontrado"},409
            

@blp.route("/cup/<int:id>")
class User(MethodView):
    @blp.response(200, CUPSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_cupon_usuario_pago,id_usuario,id_cupon,id_pago,fecha from cupon_usuario_pago where id_cupon_usario_pago={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            cup={'id_cupon_usuario_pago':datos[0],'id_usuario':datos[1],'id_cupon':datos[2],'id_pago':datos[3],'fecha':datos[4]}
            return cup,200
        else:
            return {"Mensaje": "CUP no encontrado"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from cupon_usuario_pago where id_cupon_usario_pago={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Categoria eliminada"},200

        
        
        