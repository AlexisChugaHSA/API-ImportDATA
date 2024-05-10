from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DireccionSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Direcciones", "direcciones", description="Operaciones con direcciones")

@blp.route("/direcciones")
class Direcciones_Schema(MethodView):
    @blp.response(200, DireccionSchema(many=True))
    #@jwt_required()
    def get(self):
        direcciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_direccion,id_pais, id_ciudad from direccion")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            direccion={'id_direccion':fila[0],'id_pais':fila[1],'id_ciudad':fila[2]}
            direcciones.append(direccion)
        return direcciones


@blp.route("/direccion")
class Direccion_Schema(MethodView):
    @blp.arguments(DireccionSchema)
    @blp.response(200, DireccionSchema)
    #@jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from direccion where id_pais='{0}' and id_ciudad='{1}'".format(user_data['id_pais'],user_data['id_ciudad']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into direccion(id_pais,id_ciudad) 
                        values('{0}','{1}')""".format(user_data['id_pais'],user_data['id_ciudad']))
            conexion.commit()
            with conexion.cursor() as cursor:
             cursor.execute("""SELECT * from direccion order by ID_direccion desc limit 1 """)
            datos=cursor.fetchone()
            direccion={'id_direccion':datos[0],'id_pais':datos[1],'id_ciudad':datos[2]}
            return direccion
        else:
            direccion={'id_direccion':datos[0],'id_pais':datos[1],'id_ciudad':datos[2]}
            return direccion

    @blp.arguments(DireccionSchema)     
    #@jwt_required()  
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from direccion where id_direccion='{0}'".format(user_data['id_direccion']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update direccion set id_pais='{0}', id_ciudad='{1}' where id_direccion={3}".format(user_data['id_pais'],user_data['id_ciudad'],user_data['id_direccion']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Direccion actualizada"},200
        else:
            return {"Mensaje": "Direccion no encontrada"},409
            

@blp.route("/direccion/<int:id>")
class User(MethodView):
    @blp.response(200, DireccionSchema)
    #@jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_direccion,id_pais, id_ciudad from direccion where id_direccion={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            direccion={'id_direccion':datos[0],'id_pais':datos[1],'id_ciudad':datos[2]}
            return direccion
        else:
            return {"Mensaje": "Direccion no encontrada"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from direccion where id_direccion={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Direccion eliminada"},200

        
        
        