from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MembresiasSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Membresias", "membresias", description="Operaciones con membresias")

@blp.route("/membresias")
class MembresiaSchema(MethodView):
    @blp.response(200, MembresiasSchema(many=True))
    def get(self):
        membresias=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_membresia,tipo,descuento,activo from membresias")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            membresia={'id_membresia':fila[0],'tipo':fila[1],'descuento':fila[2],'activo':fila[3]}
            membresias.append(membresia)
        return membresias


@blp.route("/membresia")
class Membresia(MethodView):
    @blp.arguments(MembresiaSchema)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from cupon where tipo='{0}'".format(user_data['tipo']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into membresias(tipo,descuento,activo) 
                        values('{0}','{1}','{2}')""".format(user_data['tipo'],user_data['descuento'],user_data['activo']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"membresia registrada"},201 
        else:
            return {"mensaje":"Ya existe una membresia de este tipo"},409

    @blp.arguments(MembresiaSchema)  
    @jwt_required()     
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from membresias where id_membresia='{0}'".format(user_data['id_membresia']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update membresias set tipo='{0}', descuento='{1}', activo='{2}' where id_membresia={3}".format(user_data['tipo'],user_data['descuento'],user_data['activo'],user_data['id_membresia']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Membresia actualizada"},200
        else:
            return {"Mensaje": "Membresia no encontrada"},409
            

@blp.route("/membresia/<int:id>")
class User(MethodView):
    @blp.response(200, MembresiasSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from membresias where id_membresia={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        #print(datos)
        if datos!=None:
            membresia={'id_membresia':datos[0],'tipo':datos[1],'descuento':datos[2],'activo':datos[3]}
            print(membresia)
            return membresia,200
        else:
            return {"Mensaje": "Membresia no encontrada"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from membresias where id_membresia={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Membresia eliminada"},200

        
        
        