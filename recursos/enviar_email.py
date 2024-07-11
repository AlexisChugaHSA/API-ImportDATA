from flask import  render_template_string, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_smorest import Blueprint
import smtplib
from email.mime.text import MIMEText

blp = Blueprint("Enviar_email", "enviar_email", description="Operaciones con correos")

# Inicializa Flask-Mail
mail = Mail()



@blp.route("/correo-bienvenida", methods=["POST"])
def enviar_correo():
    nombre_usuario = "Alexis Chuga"  # Aquí puedes obtener el nombre de usuario dinámicamente
    url_inicio = "https://tu-plataforma.com/inicio"  # URL a la que debe dirigirse el usuario
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido a nuestra plataforma de Analítica de Datos</title>
        <style>
            /* Estilos CSS */
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Bienvenido a nuestra plataforma de Analítica de Datos</h1>
            </div>
            <div class="content">
                <p>¡Hola {{ nombre }}!</p>
                <p>Estamos emocionados de tenerte como parte de nuestra comunidad.</p>
                <p>Explora datos clave, descubre tendencias y optimiza decisiones estratégicas.</p>
                <a href="{{ url}}" class="button">Comienza Ahora</a>
            </div>
        </div>
    </body>
    </html>
    """
    rendered_html = render_template_string(html_template, nombre=nombre_usuario, url=url_inicio)
    msg = Message("Bienvenida a la Plataforma", recipients=['alexis.chuga@hsa.com.ec'], sender="proyectonft867@gmail.com")
    msg.html = rendered_html 
    mail.send(msg)
    return jsonify({"message": "Correo enviado!"}), 200


@blp.route("/correo-restaurar-contrasenia", methods=["POST"])
def enviar_correo():
    msg = Message("Bienvenida", recipients=['alexis.chuga@hsa.com.ec'], sender="proyectonft867@gmail.com")
    msg.body = "Hola"
    mail.send(msg)
    return jsonify({"message": "Correo enviado!"}), 200

@blp.route("/producto-por-caducar", methods=["POST"])
def enviar_correo():
    msg = Message("Bienvenida", recipients=['alexis.chuga@hsa.com.ec'], sender="proyectonft867@gmail.com")
    msg.body = "Hola"
    mail.send(msg)
    return jsonify({"message": "Correo enviado!"}), 200