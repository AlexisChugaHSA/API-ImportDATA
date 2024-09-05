from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import EmpresaSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort, render_template, request, redirect, jsonify
blp = Blueprint("Empresas", "empresa", description="Operaciones con empresas")


@blp.route("/empresas-fact/<int:id>")
class Empresa_Schema(MethodView):
    @blp.response(200, EmpresaSchema(many=True))
    #@jwt_required()
    def get(self,id):
        empresas = []
        cursor = obtener_conexion().cursor()
        cursor.execute(
            "Select * from facturacion")
        result = cursor.fetchall()
        cursor.close()
        for fila in result:
            empresa = {'id_empresa': fila[0], 'id_metodo_pago': fila[1], 'nombre': fila[2],
                'direccion': fila[3], 'telefono': fila[4], 'correo': fila[5], 'identificacion': fila[6]}
            empresas.append(empresa)
        return empresas


@blp.route("/empresa")
class Empresaa(MethodView):
    @blp.arguments(EmpresaSchema)
    #@jwt_required()
    def post(self, user_data):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""Insert into empresa(id_metodo_pago,nombre,direccion,telefono,correo,identificacion)
                        values({0},'{1}',{2},'{3}','{4}','{5}')""".
                        format( user_data['id_metodo_pago'],user_data['nombre'], user_data['direccion'], user_data['telefono'], user_data['correo'], user_data['identificacion']))
            conexion.commit()
        with conexion.cursor() as cursor:
             cursor.execute("""SELECT * from empresa where nombre='{0}' and direccion='{1}' and telefono='{2}' and correo='{3}' and identificacion='{4}'""".
             format(user_data['nombre'],user_data['direccion'],user_data['telefono'],user_data['correo'],user_data['identificacion']))
        datos=cursor.fetchone()
        empresa={'id_empresa':datos[0],'id_metodo_pago':datos[1],'nombre':datos[2],'direccion':datos[3],'correo':datos[4],'telefono':datos[5]}
        return empresa


            

@blp.route("/empresa/<int:id>")
class User(MethodView):
    @blp.response(200, EmpresaSchema)
    #@jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_empresa,id_metodo_pago,nombre,direccion,telefono,correo,identificacion from empresa where id_empresa={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            empresa={'id_empresa':datos[0],'id_metodo_pago':datos[1],'nombre':datos[2],'direccion':datos[3],'telefono':datos[4],'correo':datos[5],'identificacion':datos[6]}
            return empresa,200
        else:
            return {"Mensaje": "Empresa no encontrada"},409
    
    @blp.arguments(EmpresaSchema)    
    #@jwt_required()   
    def put(self, user_data,id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from empresa where id_empresa={0}".format(id))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update empresa set id_metodo_pago='{0}',nombre='{1}', direccion='{2}', telefono='{3}', correo='{4}', identificacion='{5}' where id_empresa={6}".
                           format(user_data['id_metodo_pago'],user_data['nombre'],user_data['direccion'],user_data['telefono'],user_data['correo'],user_data['identificacion'],id))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Empresa actualizada"},200
        else:
            return {"Mensaje": "Empresa no encontrada"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from empresa where id_empresa={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Empresa eliminada"},200
    
@blp.route("/comprobar-empresa/<string:ruc>")
class Empresa(MethodView):
    def get(self, ruc):
        cursor = obtener_conexion().cursor()
        print(ruc)
        cursor.execute(
            "Select id_empresa from empresa where identificacion='{0}'".format(ruc))
        datos = cursor.fetchone()
        cursor.close()
        if datos != None:
            usuario = {'id_empresa': datos[0], "Mensaje": "SI"}
            return usuario, 200
        else:
            return {"Mensaje": "NOEN"}, 409

        
        
        