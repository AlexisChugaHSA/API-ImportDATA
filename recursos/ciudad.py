from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CiudadSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Ciudades", "ciudades", description="Operaciones con ciudad")

@blp.route("/ciudades")
class Ciudades_Schema(MethodView):
    @blp.response(200, CiudadSchema(many=True))
    def get(self):
        ciudades=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_ciudad,id_pais, nombre, codigo_ciudad from ciudad")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            ciudad={'id_ciudad':fila[0],'id_pais':fila[1],'nombre':fila[2],'codigo_ciudad':fila[3]}
            ciudades.append(ciudad)
        return ciudades

@blp.route("/ciudades/<int:id>")
class Ciudades_Schema(MethodView):
    @blp.response(200, CiudadSchema(many=True))
    def get(self,id):
        ciudades=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from ciudad where id_pais={0}".format(id))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            ciudad={'id_ciudad':fila[0],'id_pais':fila[1],'nombre':fila[2],'codigo_ciudad':fila[3]}
            ciudades.append(ciudad)
        return ciudades

@blp.route("/ciudad/<int:id>")
class User(MethodView):
    @blp.response(200, CiudadSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from ciudad where id_ciudad={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            ciudad={'id_ciudad':fila[0],'id_pais':fila[1],'nombre':fila[2],'codigo_ciudad':fila[3]}
            return ciudad
        else:
            return {"Mensaje": "Pais no encontrada"},409


        
        
        