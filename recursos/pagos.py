from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PagosSchema
from bd import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
from datetime import datetime, timedelta
blp = Blueprint("Pagos", "pagos", description="Operaciones con pagos")

@blp.route("/pagos")
class Pagos_Schema(MethodView):
    @blp.response(200, PagosSchema(many=True))
    @jwt_required()
    def get(self):
        pagos=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_pago,id_empresa,valor,descuento,periodo,fecha,procesado,intentos,detalle from pagos")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            pago={'id_pago':fila[0],'id_empresa':fila[1],'valor':fila[2],'descuento':fila[3],'periodo':fila[4],'fecha':fila[5],'procesado':fila[6],'intentos':fila[7],'detalle':fila[8]}
            pagos.append(pago)
        return pagos


@blp.route("/pago")
class Pago(MethodView):
    @blp.arguments(PagosSchema)
    @jwt_required()
    def post(self,user_data):
        fecha_actual = datetime.now()
        fecha_hasta = fecha_actual + timedelta(days=user_data['periodo']*30)
        fecha_hastaf= fecha_hasta.strftime('%Y-%m-%d')
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""Insert into pagos(id_empresa,valor,descuento,periodo,fecha,procesado,intentos,detalle,cancelado,fecha_hasta) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')"""
                           .format(user_data['id_empresa'],user_data['valor'],user_data['descuento'],user_data['periodo'],fecha_actual,
                                   user_data['procesado'],user_data['intentos'],user_data['detalle'],user_data['cancelado'],fecha_hastaf))
        conexion.commit()
        with conexion.cursor() as cursor:
             cursor.execute("""SELECT max(id_pago) from pagos where id_empresa='{0}' and valor='{1}' and descuento='{2}' and periodo='{3}' and fecha='{4}' and procesado='{5}' and intentos='{6}' and detalle='{7}' and cancelado='{8}' and fecha_hasta='{9}'""".
                            format(user_data['id_empresa'],user_data['valor'],user_data['descuento'],user_data['periodo'],fecha_actual,
                                   user_data['procesado'],user_data['intentos'],user_data['detalle'],user_data['cancelado'],fecha_hastaf))
        datos=cursor.fetchone()
        pago={'id_pago':datos[0]}
        #Generacion de pago pendiente
        #fecha_actual = fecha_hasta
        #fecha_hasta = fecha_actual + timedelta(days=user_data['periodo']*30)
        #fecha_hastaf= fecha_hasta.strftime('%Y-%m-%d')
        #fecha_actual = fecha_actual.strftime('%Y-%m-%d')
        #with conexion.cursor() as cursor:
         #   cursor.execute("""Insert into pagos(id_empresa,valor,descuento,periodo,fecha,procesado,intentos,detalle,cancelado,fecha_hasta) 
          #              values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')"""
           #             .format(user_data['id_empresa'],user_data['valor'],user_data['descuento'],user_data['periodo'],fecha_actual,
            #                       0,user_data['intentos'],user_data['detalle'],0,fecha_hastaf))
        #conexion.commit()
        return pago


    @blp.arguments(PagosSchema)  
    @jwt_required()     
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from pagos where id_pago='{0}'".format(user_data['id_pago']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update pagos set id_empresa='{0}', valor='{1}', descuento='{2}', periodo='{3}', fecha='{4}', procesado='{5}', intentos='{6}', detalle='{7}' where id_pago={8}"
                           .format(user_data['id_empresa'],user_data['valor'],user_data['descuento'],user_data['periodo'],user_data['fecha'],user_data['procesado'],user_data['intentos'],user_data['detalle'],user_data['id_pago']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Pago actualizado"},200
        else:
            return {"Mensaje": "Pago no encontrado"},409
            

@blp.route("/pago/<int:id>")
class Pagoo(MethodView):
    @blp.response(200, PagosSchema)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_pago,id_empresa,valor,descuento,periodo,fecha,procesado,intentos,detalle from pagos where id_pago={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            pago={'id_pago':datos[0],'id_empresa':datos[1],'valor':datos[2],'descuento':datos[3],'periodo':datos[4],'fecha':datos[5],'procesado':datos[6],'intentos':datos[7],'detalle':datos[8]}
            return pago,200
        else:
            return {"Mensaje": "Pago no encontrado"},409
    @jwt_required()
    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from pagos where id_pago={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Pago eliminado"},200

@blp.route("/pagos-empresa/<int:id>")
class Pagoo(MethodView):
    @blp.response(200, PagosSchema(many=True))
    @jwt_required()
    def get(self,id):
        pagos=[]
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from pagos where id_empresa={0}".format(id))
        datos=cursor.fetchall()
        cursor.close()
        for fila in datos:
            pago={'id_pago':fila[0],'id_empresa':fila[1],'valor':fila[2],'descuento':fila[3],'periodo':fila[4],
                  'fecha':fila[5],'procesado':fila[6],'intentos':fila[7],'detalle':fila[8],'cancelado':fila[9],'fecha_hasta':fila[10]}
            pagos.append(pago)
        return pagos,200

@blp.route("/cancelar-pago/<int:id>")
class Pagoo(MethodView):
    @jwt_required()
    def put(self,id):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        cursor.execute("Update pagos set cancelado='{0}' where id_pago={1}"
                           .format(1,id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "Pago cancelado"},200

        
        
        