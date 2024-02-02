from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DetalleFacturaSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Detalle_Factura", "detalle_factura", description="Operaciones con detalle_factura")

@blp.route("/detalle-facturas")
class CategoriaSchema(MethodView):
    @blp.response(200, DetalleFacturaSchema(many=True))
    def get(self):
        detalleFs=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_detalle_factura,id_pago,id_producto,id_factura,precio from detalle_factura")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            detalleF={'id_detalle_factura':fila[0],'id_pago':fila[1],'id_producto':fila[2],'id_factura':fila[3],'precio':fila[4]}
            detalleFs.append(detalleF)
        return detalleFs


@blp.route("/detalle-factura")
class CUP(MethodView):
    @blp.arguments(DetalleFacturaSchema)
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""Insert into detalle_factura(id_pago,id_producto,id_factura,precio) 
                        values('{0}','{1}','{2}','{3}')""".format(user_data['id_pago'],user_data['id_producto'],user_data['id_factura'],user_data['precio']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Detalle_Factura registrado"},201 


    @blp.arguments(DetalleFacturaSchema)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from detalle_factura where id_detalle_factura='{0}'".format(user_data['id_detalle_factura']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update detalle_factura set id_pago='{0}', id_producto='{1}', id_factura='{2}', precio='{3}' where id_detalle_factura={4}".
                           format(user_data['id_pago'],user_data['id_producto'],user_data['id_factura'],user_data['precio'],user_data['id_detalle_factura']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Detalle-Factura actualizado"},200
        else:
            return {"Mensaje": "Detalle-Factura no encontrado"},409
            

@blp.route("/detalle-factura/<int:id>")
class User(MethodView):
    @blp.response(200, DetalleFacturaSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_detalle_factura,id_pago,id_producto,id_factura,precio from detalle_factura where id_detalle_factura={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            dF={'id_detalle_factura':datos[0],'id_pago':datos[1],'id_producto':datos[2],'id_factura':datos[3],'precio':datos[4]}
            return dF,200
        else:
            return {"Mensaje": "CUP no encontrado"},409

    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from detalle_factura where id_detalle_factura={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Categoria eliminada"},200

@blp.route("/detalle-facturas-fact/<int:id>")
class User(MethodView):
    @blp.response(200, DetalleFacturaSchema(many=True))
    def get(self,id):
        facturacion = []
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from detalle_factura where id_factura={0}".format(id))
        datos= cursor.fetchall()
        cursor.close()
        for fila in datos:
            factura = {'id_detalle_factura':fila[0],'id_pago':fila[1],'id_producto':fila[2],'id_factura':fila[3],'precio':fila[4]}
            facturacion.append(factura)
        return facturacion

        
        
        