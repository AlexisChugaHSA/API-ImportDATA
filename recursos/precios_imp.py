from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PreciosImpSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Precios_Imp", "precios_imp", description="Operaciones con precios de importación")

@blp.route("/precios-imp")
class PreciosSch(MethodView):
    @blp.response(200, PreciosImpSch(many=True))
    @jwt_required()
    def get(self):
        precios=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from precios")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            precio={'id_precio':fila[0],'precio_contado':fila[1],'precio_cuota':fila[2],'num_cuotas':fila[3],
                    'precio_fisico':fila[4],'fecha':fila[5]}
            print (precio)
            precios.append(precio)
        return precios
    
@blp.route("/precios-imp/<int:id>")
class Precio_Imp_Sch(MethodView):
    @blp.response(200, PreciosImpSch)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from precios where id_precio={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            precio={'id_precio':fila[0],'precio_contado':fila[1],'precio_cuota':fila[2],'num_cuotas':fila[3],
                    'precio_fisico':fila[4],'fecha':fila[5]}
            print(precio)
            return precio,200
        else:
            return {"Mensaje": "Precio no encontrado"},409
        
@blp.route("/precios-imp")
class Precio_Imp(MethodView):
    @blp.arguments(PreciosImpSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into precios(precio_contado,precio_cuota,num_cuotas,precio_fisico,fecha) 
                        values('{0}','{1}','{2}','{3}','{4}')""".format(user_data['precio_contado'],user_data['precio_cuota'],user_data['num_cuotas'],
                                                                        user_data['precio_fisico'],user_data['fecha']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Precio registrado"},200


    @blp.arguments(PreciosImpSch) 
    @jwt_required()      
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from precios where id_precio={0}".format(user_data['id_precio']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update precios set precio_contado='{0}',precio_cuota='{1}',num_cuotas='{2}',precio_fisico='{3}',fecha='{4}'
                           where id_precio={5}""".format(user_data['precio_contado'],user_data['precio_cuota'],user_data['num_cuotas'],
                                                         user_data['precio_fisico'],user_data['fecha'],user_data['id_precio']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Precio actualizado"},200
        else:
            return {"Mensaje": "Precio no encontrado"},409