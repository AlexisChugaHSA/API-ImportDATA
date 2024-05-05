from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import EmpresasImpSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Empresas_Imp", "empresas_imp", description="Operaciones con empresas de importación")

@blp.route("/empresas-imp")
class EmpresasSch(MethodView):
    @blp.response(200, EmpresasImpSch(many=True))
    @jwt_required()
    def get(self):
        empresas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from empresas")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            empresa={'id_empresa':fila[0],'nombre_empresa':fila[1]}
            empresas.append(empresa)
        return empresas
    
@blp.route("/empresas-imp/<int:id>")
class EmpresaSch(MethodView):
    @blp.response(200, EmpresasImpSch)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from empresas where id_empresa={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            empresa={'id_empresa':fila[0],'nombre_empresa':fila[1]}
            return empresa,200
        else:
            return {"Mensaje": "Empresa no encontrada"},409

@blp.route("/empresas-imp")
class EmpresaImp(MethodView):
    @blp.arguments(EmpresasImpSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into empresas(nombre_empresa) 
                        values('{0}')""".format(user_data['nombre_empresa']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Empresa registrada"},200

    @blp.arguments(EmpresasImpSch)    
    @jwt_required()   
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from empresas where id_empresa={0}".format(user_data['id_empresa']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("Update empresas set nombre_empresa='{0}' where id_empresa={1}".format(user_data['nombre_empresa'],user_data['id_empresa']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Empresa actualizada"},200
        else:
            return {"Mensaje": "Empresa no encontrada"},409