from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import FacturacionSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort, render_template, request, redirect, jsonify
blp = Blueprint("Facturacion", "facturacion",
                description="Operaciones con facturacion")


@blp.route("/facturacion")
class CategoriaSchema(MethodView):
    @blp.response(200, FacturacionSchema(many=True))
    @jwt_required()
    def get(self):
        facturacion = []
        cursor = obtener_conexion().cursor()
        cursor.execute(
            "Select id_factura, id_empresa, total, subtotal, iva, iva_0 from facturacion")
        result = cursor.fetchall()
        cursor.close()
        for fila in result:
            factura = {'id_factura': fila[0], 'id_empresa': fila[1],
                'total': fila[2], 'subtotal': fila[3], 'iva': fila[4], 'iva_0': fila[5]}
            facturacion.append(factura)
        return facturacion


@blp.route("/facturacion")
class CUP(MethodView):
    @blp.arguments(FacturacionSchema)
    @jwt_required()
    def post(self, user_data):
        fecha_actual = datetime.now()
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into facturacion(id_empresa, total, subtotal,fecha, iva, iva_0)
                        values('{0}','{1}','{2}','{3}','{4}','{5}')""".format(user_data['id_empresa'], user_data['total'], user_data['subtotal'],fecha_actual, user_data['iva'], user_data['iva_0']))
        conexion.commit()
        with conexion.cursor() as cursor:
            cursor.execute("""SELECT max(id_factura) from facturacion where id_empresa='{0}' and total='{1}' and subtotal='{2}' and fecha='{3}' and iva='{4}' and iva_0='{5}' """.
                           format(user_data['id_empresa'], user_data['total'],user_data['subtotal'],fecha_actual,user_data['iva'],user_data['iva_0']))
        datos=cursor.fetchone()
        factura={'id_factura':datos[0]}
        return factura


    @blp.arguments(FacturacionSchema)
    @jwt_required()
    def put(self, user_data):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("Select * from facturacion where id_factura='{0}'".format(user_data['id_factura']))
        datos = cursor.fetchone()
        print(datos)
        if datos !=None:
            cursor.execute("Update facturacion set id_empresa='{0}', total='{1}', subtotal='{2}', iva='{3}', iva_0='{4}' where id_factura={5}".
                           format(user_data['id_empresa'], user_data['total'],user_data['subtotal'],user_data['iva'],user_data['iva_0'],user_data['id_factura']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Factura actualizada"}, 200
        else:
            return {"Mensaje": "Factura no encontrada"}, 409


@blp.route("/facturacion/<int:id>")
class User(MethodView):
    @blp.response(200, FacturacionSchema)
    @jwt_required()
    def get(self, id):
        cursor = obtener_conexion().cursor()
        cursor.execute("Select * from facturacion where id_factura={0}".format(id))
        datos = cursor.fetchone()
        cursor.close()
        if datos !=None:
            factura = {'id_factura':datos[0],'id_empresa':datos[1],'total':datos[2],'subtotal':datos[3],
                       'fecha':datos[4],'iva':datos[5],'iva_0':datos[6]}
            return factura, 200
        else:
            return {"Mensaje": "Factura no encontrada"}, 409
    @jwt_required()
    def delete(self, id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("Delete from facturacion where id_factura={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Factura eliminada"}, 200

@blp.route("/facturacionbyemp/<int:id>")
class User(MethodView):
    @blp.response(200, FacturacionSchema(many=True))
    @jwt_required()
    def get(self, id):
        facturacion = []
        cursor = obtener_conexion().cursor()
        cursor.execute("Select * from facturacion where id_empresa={0}".format(id))
        result = cursor.fetchall()
        cursor.close()
        for fila in result:
            factura = {'id_factura': fila[0], 'id_empresa': fila[1],
                'total': fila[2], 'subtotal': fila[3],'fecha': fila[4], 'iva': fila[5], 'iva_0': fila[6]}
            facturacion.append(factura)
        return facturacion
        

