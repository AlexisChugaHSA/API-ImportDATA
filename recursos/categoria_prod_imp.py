from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategoriaProductoSch
from bd_imp import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Categorias_Imp", "categorias_imp", description="Operaciones con categorias de importación")

@blp.route("/categorias-imp")
class Categorias_Imp_Schema(MethodView):
    @blp.response(200, CategoriaProductoSch(many=True))
    def get(self):
        categorias=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from categoria_producto")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            categoria={'id_categoria_producto':fila[0],'nombre_categoria_producto':fila[1]}
            categorias.append(categoria)
        return categorias

@blp.route("/categorias-imp/<int:id>")
class Categoria_Imp_Schema(MethodView):
    @blp.response(200, CategoriaProductoSch)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from categoria_producto where id_categoria_producto={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            categoria={'id_categoria_producto':fila[0],'nombre_categoria_producto':fila[1]}
            return categoria,200
        else:
            return {"Mensaje": "Categoria no encontrada"},409

@blp.route("/categorias-imp")
class CategoriaImp(MethodView):
    @blp.arguments(CategoriaProductoSch)
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from categoria_producto where nombre_categoria_producto='{0}'".format(user_data['nombre_categoria_producto']))
        datos=cursor.fetchone()
        if datos==None:
            with conexion.cursor() as cursor:
                cursor.execute("""Insert into categoria_producto(nombre_categoria_producto) 
                        values('{0}')""".format(user_data['nombre_categoria_producto']))
            conexion.commit()
            conexion.close()
            return {"mensaje":"categoria registrada"},201 
        else:
            return {"mensaje":"Ya existe una categoria con este nombre"},409

    @blp.arguments(CategoriaProductoSch)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from categoria_producto where id_categoria_producto={0}".format(user_data['id_categoria_producto']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("Update categoria_producto set nombre_categoria_producto='{0}' where id_categoria_producto={1}".format(user_data['nombre_categoria_producto'],user_data['id_categoria_producto']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Categoria actualizada"},200
        else:
            return {"Mensaje": "Categoria no encontrada"},409