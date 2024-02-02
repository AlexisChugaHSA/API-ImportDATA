from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ProductosImpSch
from bd_imp import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Productos_Imp", "productos_imp", description="Operaciones con productos de importación")

@blp.route("/productos-imp")
class Productos_Imp_Schema(MethodView):
    @blp.response(200, ProductosImpSch(many=True))
    def get(self):
        productos=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from productos")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            producto={'id_producto':fila[0],'id_precio':fila[1],'id_marca':fila[2],'id_modelo_homologado':fila[3],
                      'id_categoria_producto':fila[4],'id_tienda':fila[5],'nombre_producto':fila[6],'caracteristica_producto':fila[7]}
            productos.append(producto)
        return productos

@blp.route("/productos-imp/<int:id>")
class ProductoSch(MethodView):
    @blp.response(200, ProductosImpSch)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from productos where id_producto={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            producto={'id_producto':fila[0],'id_precio':fila[1],'id_marca':fila[2],'id_modelo_homologado':fila[3],
                      'id_categoria_producto':fila[4],'id_tienda':fila[5],'nombre_producto':fila[6],'caracteristica_producto':fila[7]}
            print(producto)
            return producto,200
        else:
            return {"Mensaje": "Precio no encontrado"},409

@blp.route("/productos-imp")
class Producto_Imp(MethodView):
    @blp.arguments(ProductosImpSch)
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into productos(id_precio,id_marca,id_modelo_homologado,id_categoria_producto,id_tienda,nombre_producto,caracteristica_producto) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')""".format(user_data['id_precio'],user_data['id_marca'],user_data['id_modelo_homologado'],
                                                                              user_data['id_categoria_producto'],user_data['id_tienda'],user_data['nombre_producto'],user_data['caracteristica']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Producto registrado"},200

    @blp.arguments(ProductosImpSch)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from productos where id_producto={0}".format(user_data['id_producto']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update productos set id_precio='{0}',id_marca='{1}',id_modelo_homologado='{2}',id_categoria_producto='{3}',id_tienda='{4}',nombre_producto='{5}',caracteristica='{6}' 
                           where id_producto={7}""".format(user_data['id_precio'],user_data['id_marca'],user_data['id_modelo_homologado'],
                                                    user_data['id_categoria_producto'],user_data['id_tienda'],user_data['nombre_producto'],
                                                    user_data['caracteristica'],user_data['id_producto']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Producto actualizado"},200
        else:
            return {"Mensaje": "Producto no encontrado"},409