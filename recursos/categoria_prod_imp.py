from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SubCategoriaProductoSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Categorias_Imp", "categorias_imp", description="Operaciones con categorias de importación")

@blp.route("/subcategorias-imp")
class Categorias_Imp_Schema(MethodView):
    @blp.response(200, SubCategoriaProductoSch(many=True))
    @jwt_required()
    def get(self):
        categorias=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from categoria_importacion")
        result=cursor.fetchall()
        print(result)
        cursor.close()
        for fila in result:
            categoria={'id_subcategoria':fila[0],'subcategoria':fila[1]}
            categorias.append(categoria)
        print(categorias)
        return categorias

@blp.route("/subcategorias-imp/<int:id>")
class Categoria_Imp_Schema(MethodView):
    @blp.response(200, SubCategoriaProductoSch(many=True))
    @jwt_required()
    def get(self,id):
        categorias=[]
        cursor= obtener_conexion().cursor()
        cursor.execute("Select distinct ID_SUBCATEGORIA from bd_importacion.importacion where id_categoria_producto={0} and ID_SUBCATEGORIA is not null".format(id))
        result=cursor.fetchall()
        print(result)
        cursor.close()
        id_subcategorias = [elemento[0] for elemento in result]
        print(id_subcategorias)
        cursor= obtener_conexion().cursor()
        cursor.execute("SELECT * FROM categoria_importacion WHERE id_subcategoria IN ({0}) ORDER BY subcategoria".format(", ".join(map(str, id_subcategorias))))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            categoria={'id_subcategoria':fila[0],'subcategoria':fila[1]}
            categorias.append(categoria)
        print(categorias)
        return categorias

@blp.route("/subcategorias-imp")
class CategoriaImp(MethodView):
    @blp.arguments(SubCategoriaProductoSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from categoria_importacion where subcategoria='{0}'".format(user_data['subcategoria']))
        datos=cursor.fetchone()
        if datos==None:
            with conexion.cursor() as cursor:
                cursor.execute("""Insert into categoria_importacion(subcategoria) 
                        values('{0}')""".format(user_data['subcategoria']))
            conexion.commit()
            conexion.close()
            return {"mensaje":"categoria registrada"},201 
        else:
            return {"mensaje":"Ya existe una categoria con este nombre"},409

    @blp.arguments(SubCategoriaProductoSch)  
    @jwt_required()     
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from categoria_importacion where id_subcategoria={0}".format(user_data['id_subcategoria']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("Update categoria_importacion set subcategoria='{0}' where id_subcategoria={1}".format(user_data['subcategoria'],user_data['id_subcategoria']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Categoria actualizada"},200
        else:
            return {"Mensaje": "Categoria no encontrada"},409