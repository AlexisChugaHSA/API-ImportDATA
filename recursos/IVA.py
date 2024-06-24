from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import IVASchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("IVA", "iva", description="Operaciones con iva")

@blp.route("/iva-s")
class DireccionSchema(MethodView):
    @blp.response(200, IVASchema(many=True))
    @jwt_required()
    def get(self):
        ivas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select iva_valor,id_iva from IVA")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            iva={'iva_valor':fila[0],'id_iva':fila[1]}
            ivas.append(iva)
        return iva


@blp.route("/iva")
class Membresia(MethodView):
    @blp.arguments(IVASchema)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from IVA where iva_valor='{0}' ".format(user_data['iva_valor']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into IVA(iva_valor) 
                        values('{1}')""".format(user_data['iva_valor']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"iva registrado"},201 
        else:
            return {"mensaje":"Ya existe un iva con ese valor"},409

    @blp.arguments(IVASchema)  
    @jwt_required()     
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from IVA where id_iva='{0}'".format(user_data['id_iva']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update IVA set iva_valor='{0}' where id_iva={1}".format(user_data['iva_valor']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "IVA actualizado"},200
        else:
            return {"Mensaje": "IVA no encontrado"},409
            

@blp.route("/iva")
class User(MethodView):
    @blp.response(200)
    @jwt_required()
    def get(self):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select iva_valor, id_iva from iva Order by id_iva DESC limit 1")
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            iva={'iva_valor':datos[0],'id_iva':datos[1]}
            return iva,200
        else:
            return {"Mensaje": "IVA no encontrado"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from iva where id_iva={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "IVA eliminado"},200

        
        
        