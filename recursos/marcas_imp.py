from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MarcasSch
from bd_imp import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Marcas_Imp", "marcas_imp", description="Operaciones con marcas de importación")

@blp.route("/marcas-imp")
class Marcas_Imp_Schema(MethodView):
    @blp.response(200, MarcasSch(many=True))
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
    @blp.response(200, MarcasSch)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from marcas where id_marca={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            marca={'id_marca':fila[0],'nombre_marca':fila[1]}
            return marca,200
        else:
            return {"Mensaje": "Empresa no encontrada"},409
        
@blp.route("/marcas-imp")
class Marcas_Imp(MethodView):
    @blp.arguments(MarcasSch)
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into marcas(nombre_marca) 
                        values('{0}')""".format(user_data['nombre_marca']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Marca registrada"},200

    @blp.arguments(MarcasSch)       
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