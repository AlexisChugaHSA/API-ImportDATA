from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ProductoSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Productos", "productos", description="Operaciones con productos")

@blp.route("/productos")
class Productos_Schema(MethodView):
    @blp.response(200, ProductoSchema(many=True))
    def get(self):
        productos=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_producto,id_categoria,nombre,descripcion,precio,descuento,url,imagen,tags from producto")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            producto={'id_producto':fila[0],'id_categoria':fila[1],'nombre':fila[2],'descripcion':fila[3],'precio':fila[4],'descuento':fila[5],'url':fila[6],'imagen':fila[7],'tags':fila[8]}
            productos.append(producto)
        return productos


@blp.route("/producto")
class Producto(MethodView):
    @blp.arguments(ProductoSchema)
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Select * from productos where id_categoria='{0}' and nombre='{1}'".format(user_data['id_categoria'],user_data['nombre']))
        datos=cursor.fetchone()
        if datos==None:
           with conexion.cursor() as cursor:
            cursor.execute("""Insert into productos(id_categoria,nombre,descripcion,precio,descuento,url,imagen,tags) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')"""
                           .format(user_data['id_categoria'],user_data['nombre'],user_data['descripcion'],user_data['precio'],user_data['descuento'],user_data['url'],user_data['imagen'],user_data['tags']))
           conexion.commit()
           conexion.close()
           return {"mensaje":"Producto registrado"},201 
        else:
            return {"mensaje":"Este producto ya se ha registrado anteriormente"},409

    @blp.arguments(ProductoSchema)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from producto where id_producto='{0}'".format(user_data['id_producto']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update pagos set id_categoria'{0}', nombre='{1}', descripcion='{2}', precio='{3}', descuento='{4}', url='{5}', imagen='{6}', tags='{7}' where id_producto={8}"
                           .format(user_data['id_categoria'],user_data['nombre'],user_data['descripcion'],user_data['precio'],user_data['descuento'],user_data['url'],user_data['imagen'],user_data['tags'],user_data['id_producto']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Producto actualizado"},200
        else:
            return {"Mensaje": "Producto no encontrado"},409
            

@blp.route("/producto/<int:id>")
class Pagoo(MethodView):
    @blp.response(200, ProductoSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_producto,id_categoria,nombre,descripcion,precio,descuento,url,imagen,tags from producto where id_producto={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            fila={'id_producto':fila[0],'id_categoria':fila[1],'nombre':fila[2],'descripcion':fila[3],'precio':fila[4],'descuento':fila[5],'url':fila[6],'imagen':fila[7],'tags':fila[8]}
            return fila,200
        else:
            return {"Mensaje": "Producto no encontrado"},409

    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from producto where id_producto={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Producto eliminado"},200

        
        
        