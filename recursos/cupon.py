from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CuponSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Cupones", "cupones", description="Operaciones con cupones")

@blp.route("/cupones")
class CuponSchema(MethodView):
    @blp.response(200, CuponSchema(many=True))
    def get(self):
        cupones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_cupon,fecha,cupon_descuento,codigo,activo from cupon")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            cupon={'id_cupon':fila[0],'fecha':fila[1],'cupon_descuento':fila[2],'codigo':fila[3],'activo':fila[4]}
            cupones.append(cupon)
        return cupones


@blp.route("/cupon")
class Categoria(MethodView):
    @blp.arguments(CuponSchema)
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from cupon where codigo='{0}'".format(user_data['codigo']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into cupon(fecha,cupon_descuento,codigo,activo) 
                        values('{0}','{1}','{2}','{3}')""".format(user_data['fecha'],user_data['cupon_descuento'],user_data['codigo'],user_data['activo']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"cupon registrado"},201 
        else:
            return {"mensaje":"Ya existe un cupon con este codigo"},409

    @blp.arguments(CuponSchema)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from cupon where codigo='{0}'".format(user_data['codigo']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update cupon set fecha='{0}', cupon_descuento='{1}', activo='{2}' where codigo={3}".format(user_data['fecha'],user_data['cupon_descuento'],user_data['activo'],user_data['codigo']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Cupon actualizado"},200
        else:
            return {"Mensaje": "Cupon no encontrado"},409
            

@blp.route("/cupon/<int:id>")
class User(MethodView):
    @blp.response(200, CuponSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_cupon,fecha,cupon_descuento,codigo,activo from cupon where id_cupon={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            cupon={'id_cupon':datos[0],'fecha':datos[1],'cupon_descuento':datos[2],'codigo':datos[3],'activo':datos[4]}
            return cupon,200
        else:
            return {"Mensaje": "Cupon no encontrado"},409

    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from cupon where id_cupon={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Cupon eliminado"},200

        
        
        