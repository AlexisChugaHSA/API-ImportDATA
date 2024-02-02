from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategoriaSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Categorias", "categorias", description="Operaciones con categorias")

@blp.route("/categorias")
class Categoria_Schema(MethodView):
    @blp.response(200, CategoriaSchema(many=True))
    def get(self):
        categorias=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_categoria,nombre,descripcion,imagen,tags from categoria")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            categoria={'id_categoria':fila[0],'nombre':fila[1],'descripcion':fila[2],'imagen':fila[3],'tags':fila[4]}
            categorias.append(categoria)
        return categorias


@blp.route("/categoria")
class Categoria(MethodView):
    @blp.arguments(CategoriaSchema)
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from categoria where nombre='{0}'".format(user_data['nombre']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into categoria(nombre,descripcion,imagen,tags) 
                        values('{0}','{1}','{2}','{3}')""".format(user_data['nombre'],user_data['descripcion'],user_data['imagen'],user_data['tags']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"categoria registrada"},201 
        else:
            return {"mensaje":"Ya existe una categoria con este nombre"},409

    @blp.arguments(CategoriaSchema)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from categoria where nombre='{0}'".format(user_data['nombre']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update categoria set nombre='{0}', descripcion='{1}', imagen='{2}', tag='{3}' where nombre={0}".format(user_data['nombre'],user_data['descripcion'],user_data['imagen'],user_data['tags']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Categoria actualizada"},200
        else:
            return {"Mensaje": "Categoria no encontrada"},409
            

@blp.route("/categoria/<int:id>")
class User(MethodView):
    @blp.response(200, CategoriaSchema)
    
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_categoria,nombre,descripcion,imagen,tags from categoria where id_categoria={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            categoria={'id_categoria':datos[0],'nombre':datos[1],'descripcion':datos[2],'imagen':datos[3],'tags':datos[4]}
            return categoria,200
        else:
            return {"Mensaje": "Categoria no encontrada"},409

    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from categoria where id_categoria={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Categoria eliminada"},200

        
        
        