import datetime
from flask import Flask, abort, render_template, request, redirect, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
import secrets
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint, abort
from bd import obtener_conexion
from flask_cors import CORS, cross_origin
from blocklist import BLOCKLIST
from recursos.usuarios import blp as UserBlueprint
from recursos.categoria import blp as CategoriaBlueprint
from recursos.cupon import blp as CuponBlueprint
from recursos.direccion import blp as DireccionBlueprint
from recursos.empresa import blp as EmpresaBlueprint
from recursos.facturacion import blp as FacturacionBlueprint
from recursos.membresias import blp as MembresiasBlueprint
from recursos.pagos import blp as PagosBlueprint
from recursos.cupon_usuario_pago import blp as CUPBlueprint
from recursos.detalle_factura import blp as DFBlueprint
from recursos.log_prod_user import blp as LPUBlueprint
from recursos.metodo_pago import blp as MPBlueprint
from recursos.persona import blp as PersonaBlueprint
from recursos.producto import blp as ProductoBlueprint
from recursos.producto_usuario import blp as PUBlueprint
from recursos.IVA import blp as IVABlueprint
from recursos.pais import blp as PaisBlueprint
from recursos.ciudad import blp as CiudadBlueprint
from recursos.categoria_prod_imp import blp as CatProdImpBlueprint
from recursos.empresas_imp import blp as EmpresasImpBlueprint
from recursos.homologacion_imp import blp as HomologacionImpBlueprint
from recursos.importador_imp import blp as ImportadorImpBlueprint
from recursos.marcas_imp import blp as MarcasImpBlueprint
from recursos.precios_imp import blp as PreciosImpBlueprint
from recursos.productos_imp import blp as ProductosImpBlueprint
from recursos.tiendas_imp import blp as TiendasImpBlueprint
from recursos.importacion_imp import blp as ImportacionImpBlueprint
from recursos.consulta_imp import blp as ConsultaImpBlueprint

app = Flask(__name__)
app.debug = True
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

# CORS(app,resources={r"/productos/*":{"origins":"http://localhost"}})
# CORS(app,resources={r"/upload/*":{"origins":"http://localhost"}})
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=50000)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.register_blueprint(UserBlueprint)
app.register_blueprint(CategoriaBlueprint)
app.register_blueprint(CuponBlueprint)
app.register_blueprint(DireccionBlueprint)
app.register_blueprint(EmpresaBlueprint)
app.register_blueprint(FacturacionBlueprint)
app.register_blueprint(MembresiasBlueprint)
app.register_blueprint(PagosBlueprint)
app.register_blueprint(CUPBlueprint)
app.register_blueprint(DFBlueprint)
app.register_blueprint(LPUBlueprint)
app.register_blueprint(MPBlueprint)
app.register_blueprint(PersonaBlueprint)
app.register_blueprint(ProductoBlueprint)
app.register_blueprint(PUBlueprint)
app.register_blueprint(IVABlueprint)
app.register_blueprint(PaisBlueprint)
app.register_blueprint(CiudadBlueprint)
app.register_blueprint(CatProdImpBlueprint)
app.register_blueprint(EmpresasImpBlueprint)
app.register_blueprint(HomologacionImpBlueprint)
app.register_blueprint(ImportadorImpBlueprint)
app.register_blueprint(MarcasImpBlueprint)
app.register_blueprint(PreciosImpBlueprint)
app.register_blueprint(ProductosImpBlueprint)
app.register_blueprint(TiendasImpBlueprint)
app.register_blueprint(ImportacionImpBlueprint)
app.register_blueprint(ConsultaImpBlueprint)


jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )


@app.route('/usuariosd/<id>', methods=['DELETE'])
@jwt_required()
def eliminar_producto(id):
    jwt = get_jwt()
    if not jwt.get("is_admin"):
        return jsonify({'mensaje': "Necesita privilegios de administrador"})
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("delete from usuario where id_usuario='{}'".format(id))
    conexion.commit()
    conexion.close()
    return jsonify({'mensaje': "usuario eliminado"})


@app.route('/login', methods=['POST'])
def login():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "Select * from usuario where usuario='{0}'".format(request.json['usuario']))
        datos = cursor.fetchone()
        print(datos)
    if datos != None and pbkdf2_sha256.verify(request.json["password"], datos[2]):
        if datos[3] == None:
            access_token = create_access_token(identity=datos[0], fresh=True)
            print(datos[0])
            with conexion.cursor() as cursor2:
                cursor2.execute("""Update usuario Set token='{0}' where id_usuario={1}""".format(
                    access_token, datos[0]))
            conexion.commit()
            conexion.close()
            # refresh_token = create_refresh_token(identity=datos[0])
            return jsonify({'mensaje': "OK", "token": access_token}), 200
        else:
            return jsonify({'mensaje': "TK"}), 200

    else:
        return jsonify({'mensaje': "NOEN"}), 200


@app.route('/login/si', methods=['POST'])
def leer_user():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "Select * from usuario where usuario='{0}'".format(request.json['usuario']))
        datos = cursor.fetchone()
    if datos != None and pbkdf2_sha256.verify(request.json["password"], datos[2]):
        with conexion.cursor() as cursor:
            cursor.execute(
                """Update usuario Set token=null where id_usuario={0}""".format(datos[0]))
            cursor.execute(
                "Select * from usuario where usuario='{0}'".format(request.json['usuario']))
            datos = cursor.fetchone()
        conexion.commit()

        access_token = create_access_token(identity=datos[0], fresh=True)
        with conexion.cursor() as cursor:
                cursor.execute("""Update usuario Set token='{0}' where id_usuario={1}""".format(
                    access_token, datos[0]))
        conexion.commit()
        conexion.close()
            # refresh_token = create_refresh_token(identity=datos[0])
        return jsonify({'mensaje': "OKSI","token":access_token}), 200
    else:
        return jsonify({'mensaje': "NOEN"})


@app.route('/logout', methods=['POST'])
@jwt_required()
def salir():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "Select * from usuario where usuario='{0}'".format(request.json['usuario']))
        datos = cursor.fetchone()
    if datos != None and pbkdf2_sha256.verify(request.json["password"], datos[2]):
        with conexion.cursor() as cursor:
            cursor.execute(
                """Update usuario Set token=null where id_usuario={0}""".format(datos[0]))
            cursor.execute(
                "Select * from usuario where usuario='{0}'".format(request.json['usuario']))
            datos = cursor.fetchone()
        conexion.commit()
        return {"message": "Successfully logged out"}, 200
    else:
        return jsonify({'mensaje': "usuario no encontrado"})


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"access_token": new_token}, 200
