from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ImportacionSch
from bd_imp import obtener_conexion
from flask_jwt_extended import jwt_required
from flask import Flask, abort,render_template, request, redirect,jsonify
blp = Blueprint("Importacion_Imp", "importacion_imp", description="Operaciones con importación")

@blp.route("/importacion-imp")
class Importacion_Imp_Schema(MethodView):
    @blp.response(200, ImportacionSch(many=True))
    @jwt_required()
    def get(self):
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("Select * from importacion")
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={'id_importacion':fila[0],'id_importador':fila[1],'id_modelo_homologado':fila[2],'id_categoria_producto':fila[3],'id_marca':fila[4],
                         'posicion_arancelaria':fila[5], 'descripcion_posicion':fila[6], 'retenciones':fila[7], 'descripcion_despacho':fila[8], 'marca':fila[9],
                         'modelo':fila[10], 'refrendo':fila[11], 'item':fila[12], 'dau':fila[13], 'fecha_despacho':fila[14],'fecha_embarque':fila[15], 
                         'fecha_llegada':fila[16], 'fecha_liquidacion':fila[17], 'fecha_pago':fila[18], 'fecha_salida_almacen':fila[19],
                         'regimen':fila[20], 'numero_manifiesto':fila[21], 'manifiesto':fila[22], 'codigo_documento_transporte':fila[23], 'documento_transporte':fila[24],
                         'aduana':fila[25], 'pais_origen':fila[26], 'pais_procedencia':fila[27], 'pais_embarque':fila[28], 'puerto_embarque':fila[29],
                         'via_transporte':fila[30], 'contenedores':fila[31], 'deposito':fila[32], 'fob':fila[33], 'flete':fila[34],
                         'seguro':fila[35], 'cif':fila[36], 'base_imponible':fila[37], 'kgs_neto':fila[38], 'kgs_bruto':fila[39],
                         'unidades':fila[40], 'tipo_unidad':fila[41], 'cantidad_comercial':fila[42], 'unidad_comercial':fila[43], 'tipo_unidad_nomenclador':fila[44],
                         'precio_unitario':fila[45], 'adval':fila[46], 'moneda':fila[47], 'embarcador':fila[48], 'codigo_liberacion':fila[49],
                         'estado_mercaderia':fila[50], 'clase_mercaderia':fila[51], 'pais_destino':fila[52], 'total_fob':fila[53], 'total_flete':fila[54],
                         'total_seguro':fila[55], 'total_cif':fila[56], 'total_kgs_neto':fila[57], 'total_kgs_bruto':fila[58], 'total_base_imponible':fila[59],
                         'total_cantidad_bultos':fila[60], 'clase':fila[61], 'verificador':fila[62], 'agente_afianzado':fila[63], 'nave':fila[64],
                         'agencia_transporte':fila[65], 'empresa_transporte':fila[66], 'aforador':fila[67], 'fecha_aforo':fila[68], 'tipo_aforo':fila[69],
                         'direccion_consignatario':fila[70], 'estado':fila[71], 'caracteristica':fila[72], 'unidad_medida':fila[73], 'caracteristica_agregada':fila[74],
                         'ranking_import':fila[75], 'modelo_homologado':fila[76]}
            importaciones.append(importacion)
        return importaciones
    
@blp.route("/importacion-imp/<int:id>")
class Categoria_Imp_Schema(MethodView):
    @blp.response(200, ImportacionSch)
    @jwt_required()
    def get(self,id):
        cursor= obtener_conexion().cursor()
        cursor.execute("Select * from importacion where id_importacion={0}".format(id))
        fila=cursor.fetchone()
        cursor.close()
        if fila!=None:
            importacion={'id_importacion':fila[0],'id_importador':fila[1],'id_modelo_homologado':fila[2],'id_categoria_producto':fila[3],'id_marca':fila[4],
                         'posicion_arancelaria':fila[5], 'descripcion_posicion':fila[6], 'retenciones':fila[7], 'descripcion_despacho':fila[8], 'marca':fila[9],
                         'modelo':fila[10], 'refrendo':fila[11], 'item':fila[12], 'dau':fila[13], 'fecha_despacho':fila[14],'fecha_embarque':fila[15], 
                         'fecha_llegada':fila[16], 'fecha_liquidacion':fila[17], 'fecha_pago':fila[18], 'fecha_salida_almacen':fila[19],
                         'regimen':fila[20], 'numero_manifiesto':fila[21], 'manifiesto':fila[22], 'codigo_documento_transporte':fila[23], 'documento_transporte':fila[24],
                         'aduana':fila[25], 'pais_origen':fila[26], 'pais_procedencia':fila[27], 'pais_embarque':fila[28], 'puerto_embarque':fila[29],
                         'via_transporte':fila[30], 'contenedores':fila[31], 'deposito':fila[32], 'fob':fila[33], 'flete':fila[34],
                         'seguro':fila[35], 'cif':fila[36], 'base_imponible':fila[37], 'kgs_neto':fila[38], 'kgs_bruto':fila[39],
                         'unidades':fila[40], 'tipo_unidad':fila[41], 'cantidad_comercial':fila[42], 'unidad_comercial':fila[43], 'tipo_unidad_nomenclador':fila[44],
                         'precio_unitario':fila[45], 'adval':fila[46], 'moneda':fila[47], 'embarcador':fila[48], 'codigo_liberacion':fila[49],
                         'estado_mercaderia':fila[50], 'clase_mercaderia':fila[51], 'pais_destino':fila[52], 'total_fob':fila[53], 'total_flete':fila[54],
                         'total_seguro':fila[55], 'total_cif':fila[56], 'total_kgs_neto':fila[57], 'total_kgs_bruto':fila[58], 'total_base_imponible':fila[59],
                         'total_cantidad_bultos':fila[60], 'clase':fila[61], 'verificador':fila[62], 'agente_afianzado':fila[63], 'nave':fila[64],
                         'agencia_transporte':fila[65], 'empresa_transporte':fila[66], 'aforador':fila[67], 'fecha_aforo':fila[68], 'tipo_aforo':fila[69],
                         'direccion_consignatario':fila[70], 'estado':fila[71], 'caracteristica':fila[72], 'unidad_medida':fila[73], 'caracteristica_agregada':fila[74],
                         'ranking_import':fila[75], 'modelo_homologado':fila[76]}
            return importacion,200
        else:
            return {"Mensaje": "Importacion no encontrada"},409

@blp.route("/importacion-imp")
class Importacion_Imp(MethodView):
    @blp.arguments(ImportacionSch)
    @jwt_required()
    def post(self,user_data):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
                cursor.execute("""Insert into importacion(id_importador,id_modelo_homologado,id_categoria_producto,id_marca,posicion_arancelaria,
                               descripcion_posicion,retenciones,descripcion_despacho,marca,modelo,refrendo,item,dau,fecha_despacho,fecha_embarque, 
                               fecha_llegada,fecha_liquidacion,fecha_pago,fecha_salida_almacen,regimen,numero_manifiesto,manifiesto,codigo_documento_transporte,
                               documento_transporte,aduana,pais_origen,pais_procedencia,pais_embarque,puerto_embarque,via_transporte,contenedores,
                               deposito,fob,flete,seguro,cif,base_imponible,kgs_neto,kgs_bruto,unidades,tipo_unidad,cantidad_comercial,unidad_comercial,
                               tipo_unidad_nomenclador,precio_unitario,adval,moneda,embarcador,codigo_liberacion,estado_mercaderia,clase_mercaderia,pais_destino,
                               total_fob,total_flete,total_seguro,total_cif,total_kgs_neto,total_kgs_bruto,total_base_imponible,total_cantidad_bultos,clase,
                               verificador,agente_afianzado,nave,agencia_transporte,empresa_transporte,aforador,fecha_aforo,tipo_aforo,direccion_consignatario,
                               estado,caracteristica,unidad_medida,caracteristica_agregada,ranking_import,modelo_homologado) 
                        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}',
                               '{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}','{37}','{38}','{39}','{40}',
                               '{41}','{42}','{43}','{44}','{45}','{46}','{47}','{48}','{49}','{50}','{51}','{52}','{53}','{54}','{55}','{56}','{57}','{58}','{59}','{60}',
                               '{61}','{62}','{63}','{64}','{65}','{66}','{67}','{68}','{69}','{70}','{71}','{72}','{73}','{74}','{75}')"""
                               .format(user_data['id_importador'],user_data['id_modelo_homologado'],user_data['id_categoria_producto'],user_data['id_marca'],
                         user_data['posicion_arancelaria'],user_data['descripcion_posicion'],user_data['retenciones'],user_data['descripcion_despacho'],user_data['marca'],
                         user_data['modelo'],user_data['refrendo'],user_data['item'],user_data['dau'],user_data['fecha_despacho'],user_data['fecha_embarque'], 
                         user_data['fecha_llegada'],user_data['fecha_liquidacion'],user_data['fecha_pago'],user_data['fecha_salida_almacen'],
                         user_data['regimen'],user_data['numero_manifiesto'],user_data['manifiesto'],user_data['codigo_documento_transporte'],user_data['documento_transporte'],
                         user_data['aduana'],user_data['pais_origen'],user_data['pais_procedencia'],user_data['pais_embarque'],user_data['puerto_embarque'],
                         user_data['via_transporte'],user_data['contenedores'],user_data['deposito'],user_data['fob'],user_data['flete'],
                         user_data['seguro'],user_data['cif'],user_data['base_imponible'],user_data['kgs_neto'],user_data['kgs_bruto'],
                         user_data['unidades'],user_data['tipo_unidad'],user_data['cantidad_comercial'],user_data['unidad_comercial'],user_data['tipo_unidad_nomenclador'],
                         user_data['precio_unitario'],user_data['adval'],user_data['moneda'],user_data['embarcador'],user_data['codigo_liberacion'],
                         user_data['estado_mercaderia'],user_data['clase_mercaderia'],user_data['pais_destino'],user_data['total_fob'],user_data['total_flete'],
                         user_data['total_seguro'],user_data['total_cif'],user_data['total_kgs_neto'],user_data['total_kgs_bruto'],user_data['total_base_imponible'],
                         user_data['total_cantidad_bultos'],user_data['clase'],user_data['verificador'],user_data['agente_afianzado'],user_data['nave'],
                         user_data['agencia_transporte'],user_data['empresa_transporte'],user_data['aforador'],user_data['fecha_aforo'],user_data['tipo_aforo'],
                         user_data['direccion_consignatario'],user_data['estado'],user_data['caracteristica'],user_data['unidad_medida'],user_data['caracteristica_agregada'],
                         user_data['ranking_import'],user_data['modelo_homologado']))
        conexion.commit()
        conexion.close()
        return {"mensaje":"Importacion registrada"},200

    @blp.arguments(ImportacionSch) 
    @jwt_required()      
    def put(self, user_data):
        conexion=obtener_conexion()
        cursor= conexion.cursor()
        cursor.execute("Select * from importacion where id_importacion={0}".format(user_data['id_importacion']))
        datos=cursor.fetchone()
        if datos!=None:
            cursor.execute("""Update importacion set id_importador='{0}',id_modelo_homologado='{1}',id_categoria_producto='{2}',id_marca='{3}',
                               descripcion_posicion='{4}',retenciones='{5}',descripcion_despacho='{6}',marca='{7}',modelo='{8}',refrendo='{9}',item='{10}',dau='{11}',fecha_despacho='{12}',fecha_embarque='{13}', 
                               fecha_llegada='{14}',fecha_liquidacion='{15}',fecha_pago='{16}',fecha_salida_almacen='{17}',regimen='{18}',numero_manifiesto='{19}',manifiesto='{20}',codigo_documento_transporte='{21}',
                               documento_transporte='{22}',aduana='{23}',pais_origen='{24}',pais_procedencia='{25}',pais_embarque='{26}',puerto_embarque='{27}',via_transporte='{28}',contenedores='{29}',
                               deposito='{30}',fob='{31}',flete='{32}',seguro='{33}',cif='{34}',base_imponible='{35}',kgs_neto='{36}',kgs_bruto='{37}',unidades='{38}',tipo_unidad='{39}',cantidad_comercial='{40}',unidad_comercial='{41}',
                               tipo_unidad_nomenclador='{42}',precio_unitario='{43}',adval='{44}',moneda='{45}',embarcador='{46}',codigo_liberacion='{47}',estado_mercaderia='{48}',clase_mercaderia='{49}',pais_destino='{50}',
                               total_fob='{51}',total_flete='{52}',total_seguro='{53}',total_cif='{54}',total_kgs_neto='{55}',total_kgs_bruto='{56}',total_base_imponible='{57}',total_cantidad_bultos='{58}',clase='{59}',
                               verificador='{60}',agente_afianzado='{61}',nave='{62}',agencia_transporte='{63}',empresa_transporte='{64}',aforador='{65}',fecha_aforo='{66}',tipo_aforo='{67}',direccion_consignatario='{68}',
                               estado='{69}',caracteristica='{70}',unidad_medida='{71}',caracteristica_agregada='{72}',ranking_import='{73}',modelo_homologado='{74}',posicion_arancelaria='{75}'
                           where id_importacion={76}""".format(user_data['id_importador'],user_data['id_modelo_homologado'],user_data['id_categoria_producto'],user_data['id_marca'],
                         user_data['descripcion_posicion'],user_data['retenciones'],user_data['descripcion_despacho'],user_data['marca'],
                         user_data['modelo'],user_data['refrendo'],user_data['item'],user_data['dau'],user_data['fecha_despacho'],user_data['fecha_embarque'], 
                         user_data['fecha_llegada'],user_data['fecha_liquidacion'],user_data['fecha_pago'],user_data['fecha_salida_almacen'],
                         user_data['regimen'],user_data['numero_manifiesto'],user_data['manifiesto'],user_data['codigo_documento_transporte'],user_data['documento_transporte'],
                         user_data['aduana'],user_data['pais_origen'],user_data['pais_procedencia'],user_data['pais_embarque'],user_data['puerto_embarque'],
                         user_data['via_transporte'],user_data['contenedores'],user_data['deposito'],user_data['fob'],user_data['flete'],
                         user_data['seguro'],user_data['cif'],user_data['base_imponible'],user_data['kgs_neto'],user_data['kgs_bruto'],
                         user_data['unidades'],user_data['tipo_unidad'],user_data['cantidad_comercial'],user_data['unidad_comercial'],user_data['tipo_unidad_nomenclador'],
                         user_data['precio_unitario'],user_data['adval'],user_data['moneda'],user_data['embarcador'],user_data['codigo_liberacion'],
                         user_data['estado_mercaderia'],user_data['clase_mercaderia'],user_data['pais_destino'],user_data['total_fob'],user_data['total_flete'],
                         user_data['total_seguro'],user_data['total_cif'],user_data['total_kgs_neto'],user_data['total_kgs_bruto'],user_data['total_base_imponible'],
                         user_data['total_cantidad_bultos'],user_data['clase'],user_data['verificador'],user_data['agente_afianzado'],user_data['nave'],
                         user_data['agencia_transporte'],user_data['empresa_transporte'],user_data['aforador'],user_data['fecha_aforo'],user_data['tipo_aforo'],
                         user_data['direccion_consignatario'],user_data['estado'],user_data['caracteristica'],user_data['unidad_medida'],user_data['caracteristica_agregada'],
                         user_data['ranking_import'],user_data['modelo_homologado'],user_data['posicion_arancelaria'],user_data['id_importacion']))
            conexion.commit()
            conexion.close()
            return {"Mensaje": "Importacion actualizado"},200
        else:
            return {"Mensaje": "Importacion no encontrado"},409