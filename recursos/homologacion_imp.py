from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import HomologacionSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Homologacion_Imp", "homologacion_imp", description="Operaciones con homologacion de importación")

@blp.route("/homologacion-imp")
class Homologaciones_Imp_Schema(MethodView):
    @blp.response(200, HomologacionSch(many=True))
    @jwt_required()
    def get(self):
        homologaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from homologacion")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            homologacion={'id_modelo_homologado':fila[0],'modelo_homologado':fila[1],'descripcion_modelo':fila[2],'caracteristica_modelo':fila[3]}
            homologaciones.append(homologacion)
        return homologaciones

@blp.route("/homologacion-imp/<int:id>")
class Homologacion_Imp_Schema(MethodView):
    @blp.response(200, HomologacionSch)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from homologacion where id_modelo_homologado={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            homologacion={'id_modelo_homologado':fila[0],'modelo_homologado':fila[1],'descripcion_modelo':fila[2],'caracteristica_modelo':fila[3]}
            return homologacion,200
        else:
            return {"Mensaje": "Homologacion no encontrada"},409

@blp.route("/homologacion-imp")
class Homolocacion_Imp(MethodView):
    @blp.arguments(HomologacionSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into homologacion(modelo_homologado,descripcion_modelo,caracteristica_modelo) 
                        values('{0}','{1}','{2}')""".format(user_data['modelo_homologado'],user_data['descripcion_modelo'],user_data['caracteristica_modelo']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Homologacion registrada"},200
    
    @blp.arguments(HomologacionSch) 
    @jwt_required()      
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from homologacion where id_modelo_homologado={0}".format(user_data['id_modelo_homologado']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update homologacion set modelo_homologado='{0}',descripcion_modelo='{1}',caracteristica_modelo='{2}' 
                           where id_modelo_homologado={3}""".format(user_data['modelo_homologado'],user_data['descripcion_modelo'],user_data['caracteristica_modelo'],user_data['id_modelo_homologado']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Homologacion actualizada"},200
        else:
            return {"Mensaje": "Homologacion no encontrada"},409