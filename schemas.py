from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id_usuario=fields.Int()
    usuario = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    token=fields.Str()

class CategoriaSchema(Schema):
    id_categoria=fields.Str()
    nombre=fields.Str(required=True)
    descripcion=fields.Str()
    imagen=fields.Str()
    tags=fields.Str()

class CuponSchema(Schema):
    id_cupon=fields.Str()
    fecha=fields.Date(required=True)
    cupon_descuento=fields.Decimal(required=True)
    codigo=fields.Str(required=True)
    activo=fields.Boolean(required=True)

class CUPSchema(Schema):
    id_cupon_usuario_pago=fields.Str()
    id_usuario=fields.Str(required=True)
    id_cupon=fields.Str(required=True)
    id_pago=fields.Str(required=True)
    fecha=fields.Date(required=True)

class DetalleFacturaSchema(Schema):
    id_detalle_factura=fields.Int()
    id_pago=fields.Int(required=True)
    id_producto=fields.Int(required=True)
    id_factura=fields.Int(required=True)
    precio=fields.Float(required=True)

class DireccionSchema(Schema):
    id_direccion=fields.Int()
    id_pais=fields.Int(required=True)
    id_ciudad=fields.Int(required=True)

class EmpresaSchema(Schema):
    id_empresa=fields.Int()
    id_metodo_pago=fields.Int()
    nombre=fields.Str(required=True)
    direccion=fields.Int(required=True)
    telefono=fields.Str(required=True)
    correo=fields.Str(required=True)
    identificacion=fields.Str(required=True)

class FacturacionSchema(Schema):
    id_factura=fields.Int()
    id_empresa=fields.Int(required=True)
    total=fields.Float(required=True)
    subtotal=fields.Float(required=True)
    fecha=fields.Str()
    iva=fields.Float(required=True)
    iva_0=fields.Float(required=True)

class IVASchema(Schema):
    id_IVA = fields.Int()
    IVA_valor=fields.Decimal(required=True)

class Log_Prod_UserSchema(Schema):
    id_log_prod_uder= fields.Int()
    id_usuario= fields.Int(required=True)
    id_producto= fields.Int(required=True)
    id_producto_usuario= fields.Int(required=True)
    precio= fields.Float(required=True)
    fecha=fields.Date(required=True)

class MembresiasSchema(Schema):
    id_membresia=fields.Int()
    tipo=fields.Str(required=True)
    descuento=fields.Float()
    activo=fields.Boolean(required=True)


class MetodoPagoSchema(Schema):
    id_metodo_pago= fields.Int()
    tarjeta=fields.Str(required=True)
    nombre=fields.Str(required=True)

class PagosSchema(Schema):
    id_pago=fields.Int()
    id_empresa=fields.Int(required=True)
    valor=fields.Float(required=True)
    descuento=fields.Decimal()
    periodo=fields.Int(required=True)
    fecha=fields.Str()
    procesado=fields.Int(required=True)
    intentos=fields.Int()
    detalle=fields.Str()
    cancelado=fields.Int()
    fecha_hasta=fields.Str()

class PaisesSchema(Schema):
    id_pais=fields.Str()
    nombre=fields.Str(required=True)
    codigo_pais=fields.Str(required=True)

class CiudadSchema(Schema):
    id_ciudad=fields.Str()
    id_pais=fields.Str()
    nombre=fields.Str(required=True)
    codigo_ciudad=fields.Str(required=True)



class PersonaSchema(Schema):
    id_persona=fields.Int()
    id_direccion=fields.Int()
    id_empresa=fields.Int()
    id_usuario=fields.Int()
    nombre=fields.Str(required=True)
    apellido=fields.Str(required=True)
    correo=fields.Str(required=True)
    telefono=fields.Str(required=True)

class ProductoSchema(Schema):
    id_producto=fields.Str()
    id_categoria=fields.Str(required=True)
    nombre=fields.Str(required=True)
    descripcion=fields.Str()
    precio=fields.Float(required=True)
    descuento=fields.Decimal()
    url=fields.Str(required=True)
    imagen=fields.Str()
    tags=fields.Str()


class ProductoUsuarioSchema(Schema):
    id_producto_usuario=fields.Int()
    id_usuario=fields.Int(required=True)
    id_producto=fields.Int(required=True)
    id_pago=fields.Int(required=True)
    activo=fields.Int(required=True)
    precio=fields.Float(required=True)
    fecha=fields.Date()
    periodo=fields.Int(required=True)
    fecha_hasta=fields.Date()

######################################################
class CategoriaProductoSch(Schema):
    id_categoria_producto=fields.Int()
    nombre_categoria_producto=fields.Str()

class EmpresasImpSch(Schema):
    id_empresa=fields.Int()
    nombre_empresa=fields.Str()

class HomologacionSch(Schema):
    id_modelo_homologado=fields.Int()
    modelo_homologado=fields.Str()
    descripcion_modelo=fields.Str()
    caracteristica_modelo=fields.Str()

class ImportacionSch(Schema):
    id_importacion=fields.Int()
    id_importador=fields.Int()
    id_modelo_homologado=fields.Int()
    id_categoria_producto=fields.Int()
    id_marca=fields.Int()
    posicion_arancelaria=fields.Str()
    descripcion_posicion=fields.Str()
    retenciones=fields.Float()
    descripcion_despacho=fields.Str()
    marca=fields.Str()
    modelo=fields.Str()
    refrendo=fields.Str()
    item=fields.Int()
    dau=fields.Str()
    fecha_despacho=fields.Date()
    fecha_embarque=fields.Date()
    fecha_llegada=fields.Date()
    fecha_liquidacion=fields.Date()
    fecha_pago=fields.Date()
    fecha_salida_almacen=fields.Date()
    regimen=fields.Str()
    numero_manifiesto=fields.Str()
    manifiesto=fields.Str()
    codigo_documento_transporte=fields.Str()
    documento_transporte=fields.Str()
    aduana=fields.Str()
    pais_origen=fields.Str()
    pais_procedencia=fields.Str()
    pais_embarque=fields.Str()
    puerto_embarque=fields.Str()
    via_transporte=fields.Str()
    contenedores=fields.Int()
    deposito=fields.Str()
    fob=fields.Float()
    flete=fields.Float()
    seguro=fields.Float()
    cif=fields.Float()
    base_imponible=fields.Float()
    kgs_neto=fields.Float()
    kgs_bruto=fields.Float()
    unidades=fields.Float()
    tipo_unidad=fields.Str()
    cantidad_comercial=fields.Int()
    unidad_comercial=fields.Str()
    tipo_unidad_nomenclador=fields.Str()
    precio_unitario=fields.Float()
    adval=fields.Float()
    moneda=fields.Str()
    embarcador=fields.Str()
    codigo_liberacion=fields.Str()
    estado_mercaderia=fields.Str()
    clase_mercaderia=fields.Str()
    pais_destino=fields.Str()
    total_fob=fields.Float()
    total_flete=fields.Float()
    total_seguro=fields.Float()
    total_cif=fields.Float()
    total_kgs_neto=fields.Float()
    total_kgs_bruto=fields.Float()
    total_base_imponible=fields.Float()
    total_cantidad_bultos=fields.Int()
    clase=fields.Str()
    verificador=fields.Str()
    agente_afianzado=fields.Str()
    nave=fields.Str()
    agencia_transporte=fields.Str()
    empresa_transporte=fields.Str()
    aforador=fields.Str()
    fecha_aforo=fields.Date()
    tipo_aforo=fields.Str()
    direccion_consignatario=fields.Str()
    estado=fields.Str()
    caracteristica=fields.Str()
    unidad_medida=fields.Str()
    caracteristica_agregada=fields.Str()
    ranking_import=fields.Str()
    modelo_homologado=fields.Str()

class ImportadorSch(Schema):
    id_importador=fields.Int()
    razon_social=fields.Str()
    potencial_uno=fields.Str()
    nombre_comercial=fields.Str()
    ruc=fields.Str()
    actividad_principal=fields.Str()
    direccion=fields.Str()

class MarcasSch(Schema):
    id_marca=fields.Int()
    nombre_marca=fields.Str()

class PreciosImpSch(Schema):
    id_precio=fields.Int()
    precio_contado=fields.Float()
    precio_cuota=fields.Float()
    num_cuotas=fields.Int()
    precio_fisico=fields.Float()
    fecha=fields.Date()

class ProductosImpSch(Schema):
    id_producto=fields.Int()
    id_precio=fields.Int()
    id_marca=fields.Int()
    id_modelo_homologado=fields.Int()
    id_categoria_producto=fields.Int()
    id_tienda=fields.Int()
    nombre_producto=fields.Str()
    caracteristica_producto=fields.Str()

class TiendasSch(Schema):
    id_tienda=fields.Int()
    id_empresa=fields.Int()
    tipo=fields.Str()
    direccion=fields.Str()

class ConsultaImpSch(Schema):
    anio=fields.List(fields.Int())
    mes=fields.List(fields.Int())
    caracteristica_modelo=fields.List(fields.Str())
    categoria=fields.List(fields.Str())
    nombre_marca=fields.List(fields.Str())
    nombre_empresa=fields.List(fields.Str())
    modelo_homologado=fields.List(fields.Str())










