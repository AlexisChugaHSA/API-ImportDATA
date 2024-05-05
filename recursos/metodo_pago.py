from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MetodoPagoSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Metodo_Pago", "metodo_pago", description="Operaciones con metodo_pago")

@blp.route("/metodos-pago")
class MetodosPagoSchema(MethodView):
    @blp.response(200, MetodoPagoSchema(many=True))
    @jwt_required()
    def get(self):
        mpagos=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_metodo_pago,tarjeta, nombre from metodopago")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            mpago={'id_metodo_pago':fila[0],'tarjeta':fila[1],'nombre':fila[2]}
            mpagos.append(mpago)
        return mpagos

@blp.route("/metodo-pago")
class MetodoPago(MethodView):
    @blp.arguments(MetodoPagoSchema)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from metodopago where tarjeta='{0}' and nombre='{1}'".format(user_data['tarjeta'],user_data['nombre']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into metodopago(tarjeta,nombre) 
                        values('{0}','{1}')""".format(user_data['tarjeta'],user_data['nombre']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"Metodo de pago registrado"},201 
        else:
            mpago={'id_metodo_pago':datos[0],'tarjeta':datos[1],'nombre':datos[2]}
            return mpago

    @blp.arguments(MetodoPagoSchema)   
    @jwt_required()    
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from metodopago where id_metodo_pago='{0}'".format(user_data['id_metodo_pago']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update metodopago set tarjeta='{0}', nombre='{1}' where id_metodo_pago={3}".format(user_data['tarjeta'],user_data['nombre'],user_data['id_metodo_pago']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Metodo de pago actualizado"},200
        else:
            return {"Mensaje": "Metodo de pago no encontrado"},409
            

@blp.route("/metodo-pago/<int:id>")
class Metodo_Pago(MethodView):
    @blp.response(200, MetodoPagoSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_metodo_pago,tarjeta, nombre from metodopago where id_metodo_pago={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            mpago={'id_metodo_pago':datos[0],'tarjeta':datos[1],'nombre':datos[2]}
            return mpago,200
        else:
            return {"Mensaje": "Metodo de pago no encontrado"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from metodopago where id_metodo_pago={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Metodo de pago eliminado"},200

        
        
        