from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MarcasSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Marcas_Imp", "marcas_imp", description="Operaciones con marcas de importación")

@blp.route("/marcas-imp")
class Marcas_Imp_Schema(MethodView):
    @blp.response(200, MarcasSch(many=True))
    @jwt_required()
    def get(self):
        marcas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from marcas")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            marca={'id_marca':fila[0],'nombre_marca':fila[1]}
            marcas.append(marca)
        return marcas
    
@blp.route("/marcas-imp/<int:id>")
class Marca_Imp_Schema(MethodView):
    @blp.response(200, MarcasSch(many=True))
    @jwt_required()
    def get(self,id):
        marcas=[]
        cursor= obtener_conexion().cursor()
        cursor.execute("Select distinct id_marca from importacion where id_categoria_producto={0}".format(id))
        result=cursor.fetchall()
        cursor.close()
        id_marcas = [elemento[0] for elemento in result]

        cursor= obtener_conexion().cursor()
        cursor.execute("SELECT * FROM marcas WHERE id_marca IN ({0}) ORDER BY NOMBRE_MARCA".format(", ".join(map(str, id_marcas))))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            marca={'id_marca':fila[0],'nombre_marca':fila[1]}
            marcas.append(marca)
        return marcas
        
@blp.route("/marcas-imp")
class Marcas_Imp(MethodView):
    @blp.arguments(MarcasSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into marcas(nombre_marca) 
                        values('{0}')""".format(user_data['nombre_marca']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Marca registrada"},200

    @blp.arguments(MarcasSch)    
    @jwt_required()   
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from marcas where id_marca={0}".format(user_data['id_marca']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("Update marcas set nombre_marca='{0}' where id_marca={1}".format(user_data['nombre_marca'],user_data['id_marca']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Marca actualizada"},200
        else:
            return {"Mensaje": "Marca no encontrada"},409 