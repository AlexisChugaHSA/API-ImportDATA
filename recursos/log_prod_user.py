from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import Log_Prod_UserSchema
from bd import obtener_conexion
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("LPU", "lpu", description="Operaciones con LPU")

@blp.route("/lpu-s")
class LogProdUserSchema(MethodView):
    @blp.response(200, Log_Prod_UserSchema(many=True))
    def get(self):
        lpus=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select id_log_prod_user,id_usuario,id_producto,id_producto_usuario, precio, fecha from log_prod_user")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            lpu={'id_log_prod_user':fila[0],'id_usuario':fila[1],'id_producto':fila[2],'id_producto_usuario':fila[3],'precio':fila[4],'fecha':fila[5]}
            lpus.append(lpu)
        return lpus


@blp.route("/lpu")
class CUP(MethodView):
    @blp.arguments(Log_Prod_UserSchema)
    def post(self,user_data):
        conexion=obtener_conexion()
        cursor=conexion.cursor()
        with conexion.cursor() as cursor:
            cursor.execute("""Insert into log_prod_user(id_usuario,id_producto,id_producto_usuario,precio,fecha) 
                        values('{0}','{1}','{2}','{3}','{4}')""".format(user_data['id_usuario'],user_data['id_producto'],user_data['id_producto_usuario'],user_data['precio'],user_data['fecha']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"LPU registrado"},201 


    @blp.arguments(Log_Prod_UserSchema)       
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from log_prod_user where id_log_prod_user='{0}'".format(user_data['id_log_prod_user']))
        datos=cursor.fetchone()
        print(datos)
        if datos!=None:
            cursor.execute("Update log_prod_user set id_usuario='{0}', id_producto='{1}', id_producto_usuario='{2}', precio='{3}', fecha='{4}' where id_log_prod_user={5}".
                           format(user_data['id_usuario'],user_data['id_producto'],user_data['id_producto_usuario'],user_data['precio'],user_data['fecha'],user_data['id_log_prod_user']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "LPU actualizado"},200
        else:
            return {"Mensaje": "LPU no encontrado"},409
            

@blp.route("/lpu/<int:id>")
class User(MethodView):
    @blp.response(200, Log_Prod_UserSchema)
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select id_log_prod_user,id_usuario,id_producto,id_producto_usuario, precio, fecha from log_prod_user where id_log_prod_user={0}".format(id))
        datos=cursor.fetchone()
        cursor.close()
        if datos!=None:
            lpu={'id_log_prod_user':datos[0],'id_usuario':datos[1],'id_producto':datos[2],'id_producto_usuario':datos[3],'precio':datos[4],'fecha':datos[5]}
            return lpu,200
        else:
            return {"Mensaje": "LPU no encontrado"},409

    def delete(self, id):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Delete from log_prod_user where id_log_prod_user={0}".format(id))
        conexion.commit()
        conexion.close()
        return {"Mensaje": "LPU eliminada"},200

        
        
        