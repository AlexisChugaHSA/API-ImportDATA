from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TiendasSch
from bd_imp import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Tiendas_Imp", "tiendas_imp", description="Operaciones con tiendas de importación")

@blp.route("/tiendas-imp")
class Tiendas_Imp_Schema(MethodView):
    @blp.response(200, TiendasSch(many=True))
    def get(self):
        tiendas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from tiendas")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            tienda={'id_tienda':fila[0],'id_empresa':fila[1],'tipo':fila[2],'direccion':fila[3]}
            tiendas.append(tienda)
        return tiendas

@blp.route("/tiendas-imp/<int:id>")
class TiendaSch(MethodView):
    @blp.response(200, TiendasSch)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from tiendas where id_tienda={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            tienda={'id_tienda':fila[0],'id_empresa':fila[1],'tipo':fila[2],'direccion':fila[3]}
            return tienda,200
        else:
            return {"Mensaje": "Precio no encontrado"},409

@blp.route("/tiendas-imp")
class Tienda_Imp(MethodView):
    @blp.arguments(TiendasSch)
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into tiendas(id_empresa,tipo,direccion) 
                        values('{0}','{1}','{2}')""".format(user_data['id_empresa'],user_data['tipo'],user_data['direccion']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Tienda registrada"},200

    @blp.arguments(TiendasSch)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from tiendas where id_tienda={0}".format(user_data['id_tienda']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update tiendas set id_empresa='{0}',tipo='{1}',direccion='{2}' 
                           where id_tienda={3}""".format(user_data['id_empresa'],user_data['tipo'],user_data['direccion'],user_data['id_tienda']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Tienda actualizada"},200
        else:
            return {"Mensaje": "Tienda no encontrada"},409