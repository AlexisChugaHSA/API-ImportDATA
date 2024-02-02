from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PaisesSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Paises", "paises", description="Operaciones con paises")

@blp.route("/paises")
class Paises_Schema(MethodView):
    @blp.response(200, PaisesSchema(many=True))
    def get(self):
        paises=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_pais, nombre, codigo_pais from paises")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            pais={'id_pais':fila[0],'nombre':fila[1],'codigo_pais':fila[2]}
            paises.append(pais)
        return paises

@blp.route("/pais/<int:id>")
class User(MethodView):
    @blp.response(200, PaisesSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_pais, nombre, codigo_pais from paises where id_pais={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            pais={'id_pais':datos[0],'nombre':datos[1],'codigo_pais':datos[2]}
            return pais
        else:
            return {"Mensaje": "Pais no encontrada"},409


        
        
        