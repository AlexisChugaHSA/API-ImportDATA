from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import FacturacionSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort, render_template, request, redirect, jsonify
blp = Blueprint("Facturacion", "facturacion",
                description="Operaciones con facturacion")


@blp.route("/facturas-by-user/<int:id>")
class CategoriaSchema(MethodView):
    @blp.response(200, FacturacionSchema(many=True))
    @jwt_required()
    def get(self,id):
        facturacion = []
        cursor = obtener_conexion().cursor()
        cursor.execute(
            "Select * from facturacion where id_usuario={0}".format(id))
        result = cursor.fetchall()
        cursor.close()
        for datos in result:
            factura = {'id_factura':datos[0],'id_empresa':datos[1],'total':datos[2],'subtotal':datos[3],
                       'fecha':datos[4],'iva':datos[5],'iva_0':datos[6],'ruc_empresa':datos[7],'nombre_empresa':datos[8],
                       'telefono_empresa':datos[9],'correo_empresa':datos[10],'id_usuario':datos[11]}
            facturacion.append(factura)
        return facturacion


@blp.route("/facturacion")
class CUP(MethodView):
    @blp.arguments(FacturacionSchema)
    #@jwt_required()
    def post(self, user_data):
        fecha_actual = datetime.now()
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        print(user_data)
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into facturacion(id_empresa, total, subtotal,fecha, iva, iva_0,ruc_empresa,nombre_empresa,telefono_empresa,correo_empresa,id_usuario)
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')""".
                        format(user_data['id_empresa'], user_data['total'],user_data['subtotal'],fecha_actual, 
                               user_data['iva'], user_data['iva_0'], user_data['ruc_empresa'], user_data['nombre_empresa'], user_data['telefono_empresa'],
                               user_data['correo_empresa'], user_data['id_usuario']))
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
                       'fecha':datos[4],'iva':datos[5],'iva_0':datos[6],'ruc_empresa':datos[7],'nombre_empresa':datos[8],
                       'telefono_empresa':datos[9],'correo_empresa':datos[10],'id_usuario':datos[11]}
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
        cursor.execute("Select * from facturacion where id_usuario={0}".format(id))
        result = cursor.fetchall()
        cursor.close()
        for datos in result:
            factura = {'id_factura':datos[0],'id_empresa':datos[1],'total':datos[2],'subtotal':datos[3],
                       'fecha':datos[4],'iva':datos[5],'iva_0':datos[6],'ruc_empresa':datos[7],'nombre_empresa':datos[8],
                       'telefono_empresa':datos[9],'correo_empresa':datos[10],'id_usuario':datos[11]}
            facturacion.append(factura)
        return facturacion
        

