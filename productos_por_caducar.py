import logging
from bd import obtener_conexion
from flask import Flask, render_template_string
from flask_mail import Mail, Message
import os
import datetime

logging.basicConfig(level=logging.INFO)

app1 = Flask(__name__)

app1.config['MAIL_SERVER'] = 'smtp.example.com'
app1.config['MAIL_PORT'] = 587
app1.config['MAIL_USERNAME'] = 'proyectonft867@gmail.com'
app1.config['MAIL_PASSWORD'] = 'wzmw szqf lbdf voov'
app1.config['MAIL_USE_TLS'] = True

mail = Mail(app1)

def enviar_email_caducidad():
    logging.info("Iniciando el proceso de envío de correos electrónicos")
    fecha_actual = datetime.datetime.now().date()
    logging.info(f"Fecha actual: {fecha_actual}")
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

    logging.info(f"Productos próximos a caducar encontrados: {len(registros)}")

    if not registros:
        logging.info("No hay productos próximos a caducar.")
        return

    usuarios_productos = {}

    for registro in registros:
        usuario, nombre_producto, fecha_hasta = registro
        if usuario not in usuarios_productos:
            usuarios_productos[usuario] = []
        usuarios_productos[usuario].append({
            'nombre': nombre_producto,
            'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d')
        })

    with app1.app_context():
        for usuario, productos in usuarios_productos.items():
            msg = Message("¡Aviso Importante sobre la Caducidad de tus Productos!", 
                          recipients=[usuario], 
                          sender='proyectonft867@gmail.com')
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
            logging.info(f"Correo enviado a: {usuario}")

if __name__ == "__main__":
    enviar_email_caducidad()
