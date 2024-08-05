from flask import  render_template_string, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_smorest import Blueprint
import smtplib
from bd import obtener_conexion
from email.mime.text import MIMEText
import random
import string
import os
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

blp = Blueprint("Enviar_email", "enviar_email", description="Operaciones con correos")

# Inicializa Flask-Mail
mail = Mail()



@blp.route("/correo-bienvenida")
class CorreoBienvenida(MethodView):
    def post(self):
        user_data=request.get_json()
        html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div style="text-align: center; font-family: Arial, sans-serif;">
            <h1 style="color: #f26723;">¡Bienvenido a Nuestra Plataforma de Analítica!</h1>
            <p>Estamos encantados de darte la bienvenida a nuestra plataforma de analítica. Nos enorgullece que hayas elegido nuestra solución para tus necesidades de análisis de datos y estamos comprometidos a ofrecerte la mejor experiencia posible.</p>
            
            <p>Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos. ¡Estamos aquí para ayudarte!</p>
            
            <a href="http://www.hsa.com.ec" style="color: #f26723;">www.hsa.com.ec</a>
        </div>
        <div style="font-size: small; color: gray; text-align: center; margin-top: 20px;">
            <p>COMUNICACIÓN CONFIDENCIAL Y PRIVILEGIADA. Si usted no es la persona a quien se dirige esta comunicación o no está autorizada para leerla, favor notifíquenos por e-mail y elimine todas las copias del mensaje. Se prohíbe su reproducción, publicación o entrega por cualquier medio sin el consentimiento y autorización previa y escrita del remitente de la comunicación. Este mensaje es un mensaje confidencial y privilegiado entre hsa - cliente.</p>
            <p>CONFIDENTIAL AND PRIVILEGED COMMUNICATION. If you have received this message in error or you are not authorized, please notify me by return e-mail, and destroy all copies (electronic or otherwise) of this mailing. Its reproduction, publication and/or sending by any means is prohibited unless the prior written approval of the message sender. This message shall be an hsa - client privileged communication.</p>
        </div>
    </body>
    </html>
        """
        rendered_html = render_template_string(html_template)
        msg = Message("¡Bienvenido a Nuestra Plataforma de Analítica!", recipients=[user_data['correo_usuario']], sender=os.getenv('EMAIL_USER'))
        msg.html = rendered_html 
        mail.send(msg)
        return jsonify({"message": "Correo de bienvenida enviado !"}), 200


@blp.route("/correo-restaurar-contrasenia/<int:id>", methods=["POST"])
def enviar_correo(id):
    user_data=request.get_json()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    caracteres = string.ascii_letters + string.digits
    contrasena_aux = ''.join(random.choice(caracteres) for _ in range(8))
    contrasena = pbkdf2_sha256.hash(contrasena_aux)
    cursor.execute("Update usuario set password='{0}' where id_usuario={1}".format( contrasena, id))
    conexion.commit()
    conexion.close()
    msg = Message("Restaura tu contraseña", recipients=[user_data['correo_usuario']], sender=os.getenv('EMAIL_USER'))
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    
</head>
<body>
    <div style="text-align: center; font-family: Arial, sans-serif;">
        <h1 style="color: #f26723;">Contraseña Temporal</h1>
        <p>Hemos recibido una solicitud para restablecer tu contraseña. Hemos generado una contraseña temporal para que puedas acceder a tu cuenta. Te recomendamos cambiar esta contraseña temporal por una nueva tan pronto como inicies sesión.</p>
        <p style="font-weight: bold;">Tu contraseña temporal es: <span style="background-color: #f2f2f2; padding: 5px; border-radius: 5px;">{}</span></p>
        <p>Inicia sesión en tu cuenta utilizando la contraseña temporal</p>
        <p>Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos. ¡Estamos aquí para ayudarte!</p>
        
        <a href="http://www.hsa.com.ec" style="color: #f26723;">www.hsa.com.ec</a></p>
    </div>
    <div style="font-size: small; color: gray; text-align: center; margin-top: 20px;">
        <p>COMUNICACIÓN CONFIDENCIAL Y PRIVILEGIADA. Si usted no es la persona a quien se dirige esta comunicación o no está autorizada para leerla, favor notifíquenos por e-mail y elimine todas las copias del mensaje. Se prohíbe su reproducción, publicación o entrega por cualquier medio sin el consentimiento y autorización previa y escrita del remitente de la comunicación. Este mensaje es un mensaje confidencial y privilegiado entre hsa - cliente.</p>
        <p>CONFIDENTIAL AND PRIVILEGED COMMUNICATION. If you have received this message in error or you are not authorized, please notify me by return e-mail, and destroy all copies (electronic or otherwise) of this mailing. Its reproduction, publication and/or sending by any means is prohibited unless the prior written approval of the message sender. This message shall be an hsa - client privileged communication.</p>
    </div>
</body>
</html>""".format(contrasena_aux)
    rendered_html = render_template_string(html_template)
    msg.html = rendered_html 
    mail.send(msg)
    return jsonify({"message": "Correo de resetear contraseña enviado!"}), 200

@blp.route("/producto-por-caducar", methods=["POST"])
def enviar_correo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query_select = """
    SELECT 
        u.USUARIO,
        p.NOMBRE AS NOMBRE_PRODUCTO,
        pu.FECHA_HASTA
    FROM 
        bd_import_pricing.producto_usuario pu
    JOIN 
        bd_import_pricing.producto p ON pu.ID_PRODUCTO = p.ID_PRODUCTO
    JOIN 
        bd_import_pricing.usuario u ON pu.ID_USUARIO = u.ID_USUARIO
    WHERE 
        pu.FECHA_HASTA = DATE_ADD(CURDATE(), INTERVAL 5 DAY)
    ORDER BY 
        u.USUARIO;
    """
    cursor.execute(query_select)
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    if not registros:
        return "No hay productos próximos a caducar."

    usuarios_productos = {}

    for registro in registros:
        usuario, nombre_producto, fecha_hasta = registro
        if usuario not in usuarios_productos:
            usuarios_productos[usuario] = []
        usuarios_productos[usuario].append({
            'nombre': nombre_producto,
            'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d')
        })

    for usuario, productos in usuarios_productos.items():
            msg = Message("¡Aviso Importante sobre la Caducidad de tus Productos!", 
                          recipients=[usuario], 
                          sender=os.getenv('EMAIL_USER'))
            html_template = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <div style="text-align: center; font-family: Arial, sans-serif;">
                    <h1 style="color: #ff6347;">¡Aviso Importante sobre la Caducidad de tus Productos!</h1>
                    <p>Estimado cliente,</p>
                    <p>Queremos informarte que algunos de los productos en tu cuenta están próximos a caducar. Es importante que revises y tomes las acciones necesarias para evitar cualquier inconveniente.</p>
                    <p style="font-weight: bold;">Productos próximos a caducar:</p>
                    <ul style="list-style-type: none; padding: 0;">
                        {% for producto in productos %}
                            <li style="background-color: #f2f2f2; padding: 10px; margin: 5px; border-radius: 5px;">
                                {{ producto['nombre'] }} - Fecha de caducidad: {{ producto['fecha_hasta'] }} 
                            </li>
                        {% endfor %}
                    </ul>
                    <p>Para más detalles, por favor revisa tu cuenta o contacta a nuestro equipo de soporte.</p>
                    <p>Gracias por tu atención.</p>
                    <a href="http://www.hsa.com.ec" style="color: #ff6347;">www.hsa.com.ec</a>
                </div>
                <div style="font-size: small; color: gray; text-align: center; margin-top: 20px;">
                    <p>COMUNICACIÓN CONFIDENCIAL Y PRIVILEGIADA. Si usted no es la persona a quien se dirige esta comunicación o no está autorizada para leerla, favor notifíquenos por e-mail y elimine todas las copias del mensaje. Se prohíbe su reproducción, publicación o entrega por cualquier medio sin el consentimiento y autorización previa y escrita del remitente de la comunicación. Este mensaje es un mensaje confidencial y privilegiado entre hsa - cliente.</p>
                    <p>CONFIDENTIAL AND PRIVILEGED COMMUNICATION. If you have received this message in error or you are not authorized, please notify me by return e-mail, and destroy all copies (electronic or otherwise) of this mailing. Its reproduction, publication and/or sending by any means is prohibited unless the prior written approval of the message sender. This message shall be an hsa - client privileged communication.</p>
                </div>
            </body>
            </html>
            """
            rendered_html = render_template_string(html_template, productos=productos)
            msg.html = rendered_html 
            mail.send(msg)
    return jsonify({"message": "Correo enviado!"}), 200
