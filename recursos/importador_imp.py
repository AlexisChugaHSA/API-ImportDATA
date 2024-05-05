from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ImportadorSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Importador_Imp", "importador_imp", description="Operaciones con importadores")

@blp.route("/importador-imp")
class Importadores_Imp_Schema(MethodView):
    @blp.response(200, ImportadorSch(many=True))
    @jwt_required()
    def get(self):
        importadores=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from importador")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importador={'id_importador':fila[0],'razon_social':fila[1],'potencial_uno':fila[2],'nombre_comercial':fila[3],
                        'ruc':fila[4],'actividad_principal':fila[5],'direccion':fila[6]}
            importadores.append(importador)
        return importadores
    
@blp.route("/importador-imp/<int:id>")
class Importador_Imp_Schema(MethodView):
    @blp.response(200, ImportadorSch)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from importador where id_importador={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            importador={'id_importador':fila[0],'razon_social':fila[1],'potencial_uno':fila[2],'nombre_comercial':fila[3],
                        'ruc':fila[4],'actividad_principal':fila[5],'direccion':fila[6]}
            return importador,200
        else:
            return {"Mensaje": "Empresa no encontrada"},409

@blp.route("/importador-imp")
class Importador_Imp(MethodView):
    @blp.arguments(ImportadorSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into importador(razon_social,potencial_uno,nombre_comercial,ruc,actividad_principal,direccion) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}')""".format(user_data['razon_social'],user_data['potencial_uno'],user_data['nombre_comercial'],
                                                                              user_data['ruc'],user_data['actividad_principal'],user_data['direccion']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Importador registrado"},200

    @blp.arguments(ImportadorSch) 
    @jwt_required()      
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from importador where id_importador={0}".format(user_data['id_importador']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update importador set razon_social='{0}',potencial_uno='{1}',nombre_comercial='{2}',ruc='{3}',actividad_principal='{4}',direccion='{5}' 
                           where id_importador={6}""".format(user_data['razon_social'],user_data['potencial_uno'],user_data['nombre_comercial'],
                                                            user_data['ruc'],user_data['actividad_principal'],user_data['direccion'],user_data['id_importador']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Importador actualizado"},200
        else:
            return {"Mensaje": "Importador no encontrado"},409