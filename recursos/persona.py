from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PersonaSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Personas", "persona", description="Operaciones con personas")

@blp.route("/personas")
class Personas(MethodView):
    @blp.response(200, PersonaSchema(many=True))
    @jwt_required()
    def get(self):
        personas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_persona,id_direccion,id_empresa,id_usuario,nombre,apellido,correo,telefono from persona")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            persona={'id_persona':fila[0],'id_direccion':fila[1],'id_empresa':fila[2],'id_usuario':fila[3],'nombre':fila[4],'apellido':fila[5],'correo':fila[6],'telefono':fila[7]}
            personas.append(persona)
        return personas


@blp.route("/persona")
class Persona(MethodView):
    @blp.arguments(PersonaSchema)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from persona where correo='{0}'".format(user_data['correo']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
           
            ##cursor.execute("""Insert into persona(id_direccion,id_empresa,id_usuario,nombre,apellido,correo,telefono) 
                        #values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')""".
                        #format(user_data['id_direccion'],user_data['id_empresa'],user_data['id_usuario'],user_data['nombre'],user_data['apellido'],user_data['correo'],user_data['telefono']))
            cursor.execute("""Insert into persona(id_direccion,id_empresa,id_usuario,nombre,apellido,correo,telefono) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')""".
                        format(user_data['id_direccion'],user_data['id_empresa'],user_data['id_usuario'],user_data['nombre'],user_data['apellido'],user_data['correo'],user_data['telefono']))
           print(user_data)
           conexion.commit()
           conexion.close()
           
           return user_data,201 
        else:
            return {"mensaje":"Ya existe una persona con este correo"},409


            

@blp.route("/persona/<int:id>")
class Person(MethodView):
    @blp.response(200, PersonaSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_persona,id_direccion,id_empresa,id_usuario,nombre,apellido,correo,telefono from persona where id_persona={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            persona={'id_persona':fila[0],'id_direccion':fila[1],'id_empresa':fila[2],'id_usuario':fila[3],'nombre':fila[4],'apellido':fila[5],'correo':fila[6],'telefono':fila[7]}
            return persona,200
        else:
            return {"Mensaje": "Persona no encontrada"},409
    
    @blp.arguments(PersonaSchema) 
    @jwt_required()      
    def put(self,user_data, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from persona where id_persona='{0}'".format(id))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update persona set id_direccion='{0}',id_empresa='{1}', id_usuario='{2}', nombre='{3}', apellido='{4}', correo='{5}',telefono='{6}' where id_persona={7}".
                           format(user_data['id_direccion'],user_data['id_empresa'],user_data['id_usuario'],user_data['nombre'],user_data['apellido'],user_data['correo'],user_data['telefono'],id))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Datos actualizados con éxito"},200
        else:
            return {"Mensaje": "No se ha podido actalizar los datos"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from persona where id_persona={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Persona eliminada"},200


@blp.route("/persona-by-user/<int:id>")
class Person(MethodView):
    @blp.response(200, PersonaSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_persona,id_direccion,id_empresa,id_usuario,nombre,apellido,correo,telefono from persona where id_usuario={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            persona={'id_persona':fila[0],'id_direccion':fila[1],'id_empresa':fila[2],'id_usuario':fila[3],'nombre':fila[4],'apellido':fila[5],'correo':fila[6],'telefono':fila[7]}
            return persona,200
        else:
            return {"Mensaje": "Persona no encontrada"},409
        
        
        