import datetime

from flask import jsonify
from flask_jwt_extended import jwt_required
from blocklist import BLOCKLIST
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ConsultaImpSch
from bd_imp import obtener_conexion

blp = Blueprint("Consulta_Imp", "consulta_imp", description="Operaciones con importación")
        
@blp.route("/consultas-imp")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "WHERE 1"  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil

        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_empresa' in user_data and isinstance(user_data['nombre_empresa'], list) and len(user_data['nombre_empresa']) > 0:
            where_clause += " AND nombre_empresa IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_empresa']]))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica_modelo' in user_data and isinstance(user_data['caracteristica_modelo'], list) and len(user_data['caracteristica_modelo']) > 0:
            where_clause += " AND caracteristica_modelo IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['caracteristica_modelo']]))
        if 'modelo_homologado' in user_data and isinstance(user_data['modelo_homologado'], list) and len(user_data['modelo_homologado']) > 0:
            where_clause += " AND modelo_homologado IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['modelo_homologado']]))
        if 'categoria' in user_data and isinstance(user_data['categoria'], list) and len(user_data['categoria']) > 0:
            where_clause += " AND categoria IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['categoria']]))


        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""Select posicion_arancelaria,descripcion_posicion,retenciones,descripcion_despacho,marca,modelo,refrendo,item,dau,fecha_despacho,fecha_embarque, 
                               fecha_llegada,fecha_liquidacion,fecha_pago,fecha_salida_almacen,regimen,numero_manifiesto,manifiesto,codigo_documento_transporte,
                               documento_transporte,aduana,pais_origen,pais_procedencia,pais_embarque,puerto_embarque,via_transporte,contenedores,
                               deposito,fob,flete,seguro,cif,base_imponible,kgs_neto,kgs_bruto,unidades,tipo_unidad,cantidad_comercial,unidad_comercial,
                               tipo_unidad_nomenclador,precio_unitario,adval,moneda,embarcador,codigo_liberacion,estado_mercaderia,clase_mercaderia,pais_destino,
                               total_fob,total_flete,total_seguro,total_cif,total_kgs_neto,total_kgs_bruto,total_base_imponible,total_cantidad_bultos,clase,
                               verificador,agente_afianzado,nave,agencia_transporte,empresa_transporte,aforador,fecha_aforo,tipo_aforo,direccion_consignatario,
                               estado,caracteristica,unidad_medida,caracteristica_agregada,ranking_import,importacion.modelo_homologado,nombre_marca,razon_social,
                               potencial_uno,nombre_comercial,ruc,actividad_principal,direccion_importador,homologacion.modelo_homologado,descripcion_modelo,caracteristica_modelo,
                               nombre_categoria_producto,nombre_empresa
                               from importacion 
                               join marcas on importacion.id_marca = marcas.id_marca
                               join importador on importacion.id_importador = importador.id_importador
                               join homologacion on importacion.id_modelo_homologado = homologacion.id_modelo_homologado
                               join categoria_producto on importacion.id_categoria_producto = categoria_producto.id_categoria_producto
                               join productos on categoria_producto.id_categoria_producto = productos.id_categoria_producto
                               join tiendas on productos.id_tienda = productos.id_tienda
                               join empresas on tiendas.id_empresa = empresas.id_empresa
                               {0}  
                               
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'posicion_arancelaria':fila[0], 'descripcion_posicion':fila[1], 'retenciones':fila[2], 'descripcion_despacho':fila[3], 'marca':fila[4],
                         'modelo':fila[5], 'refrendo':fila[6], 'item':fila[7], 'dau':fila[8], 'fecha_despacho':fila[9].strftime('%Y-%m-%d'),'fecha_embarque':fila[10].strftime('%Y-%m-%d'), 
                         'fecha_llegada': fila[11].strftime('%Y-%m-%d'), 'fecha_liquidacion':fila[12].strftime('%Y-%m-%d'), 'fecha_pago':fila[13].strftime('%Y-%m-%d'), 'fecha_salida_almacen':fila[14].strftime('%Y-%m-%d'),
                         'regimen':fila[15], 'numero_manifiesto':fila[16], 'manifiesto':fila[17], 'codigo_documento_transporte':fila[18], 'documento_transporte':fila[19],
                         'aduana':fila[20], 'pais_origen':fila[21], 'pais_procedencia':fila[22], 'pais_embarque':fila[23], 'puerto_embarque':fila[24],
                         'via_transporte':fila[25], 'contenedores':fila[26], 'deposito':fila[27], 'fob':fila[28], 'flete':fila[29],
                         'seguro':fila[30], 'cif':fila[31], 'base_imponible':fila[32], 'kgs_neto':fila[33], 'kgs_bruto':fila[34],
                         'unidades':fila[35], 'tipo_unidad':fila[36], 'cantidad_comercial':fila[37], 'unidad_comercial':fila[38], 'tipo_unidad_nomenclador':fila[39],
                         'precio_unitario':fila[40], 'adval':fila[41], 'moneda':fila[42], 'embarcador':fila[43], 'codigo_liberacion':fila[44],
                         'estado_mercaderia':fila[45], 'clase_mercaderia':fila[46], 'pais_destino':fila[47], 'total_fob':fila[48], 'total_flete':fila[49],
                         'total_seguro':fila[50], 'total_cif':fila[51], 'total_kgs_neto':fila[52], 'total_kgs_bruto':fila[53], 'total_base_imponible':fila[54],
                         'total_cantidad_bultos':fila[55], 'clase':fila[56], 'verificador':fila[57], 'agente_afianzado':fila[58], 'nave':fila[59],
                         'agencia_transporte':fila[60], 'empresa_transporte':fila[61], 'aforador':fila[62], 'fecha_aforo':fila[63].strftime('%Y-%m-%d'), 'tipo_aforo':fila[64],
                         'direccion_consignatario':fila[65], 'estado':fila[66], 'caracteristica':fila[67], 'unidad_medida':fila[68], 'caracteristica_agregada':fila[69],
                         'ranking_import':fila[70], 'modelo_homologado':fila[71],'nombre_marca':fila[72],'razon_social':fila[73],'potencial_uno':fila[74],
                         'nombre_comercial':fila[75],'ruc':fila[76],'actividad_principal':fila[77],'direccion_importador':fila[78],'modelo_homologado_hm':fila[79],
                         'descripcion_modelo':fila[80],'caracteristica_modelo':fila[81],'nombre_categoria_producto':fila[82],'nombre_empresa':fila[83]}
            importaciones.append(importacion)
        return importaciones

@blp.route("/consulta-imp")
class Consulta_Imp(MethodView):
   # @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "WHERE 1"  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil

        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))


        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""Select posicion_arancelaria,descripcion_posicion,retenciones,descripcion_despacho,marca,modelo,refrendo,item,dau,fecha_despacho,fecha_embarque, 
                               fecha_llegada,fecha_liquidacion,fecha_pago,fecha_salida_almacen,regimen,numero_manifiesto,manifiesto,codigo_documento_transporte,
                               documento_transporte,aduana,pais_origen,pais_procedencia,pais_embarque,puerto_embarque,via_transporte,contenedores,
                               deposito,fob,flete,seguro,cif,base_imponible,kgs_neto,kgs_bruto,unidades,tipo_unidad,cantidad_comercial,unidad_comercial,
                               tipo_unidad_nomenclador,precio_unitario,adval,moneda,embarcador,codigo_liberacion,estado_mercaderia,clase_mercaderia,pais_destino,
                               total_fob,total_flete,total_seguro,total_cif,total_kgs_neto,total_kgs_bruto,total_base_imponible,total_cantidad_bultos,clase,
                               verificador,agente_afianzado,nave,agencia_transporte,empresa_transporte,aforador,fecha_aforo,tipo_aforo,direccion_consignatario,
                               estado,caracteristica,unidad_medida,caracteristica_agregada,ranking_import,modelo_homologado
                               from importacion 
                               join marcas on importacion.id_marca = marcas.id_marca
                               {0} 
                               
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'posicion_arancelaria':fila[0], 'descripcion_posicion':fila[1], 'retenciones':fila[2], 'descripcion_despacho':fila[3], 'marca':fila[4],
                         'modelo':fila[5], 'refrendo':fila[6], 'item':fila[7], 'dau':fila[8], 'fecha_despacho':fila[9],'fecha_embarque':fila[10], 
                         'fecha_llegada': fila[11], 'fecha_liquidacion':fila[12], 'fecha_pago':fila[13], 'fecha_salida_almacen':fila[14],
                         'regimen':fila[15], 'numero_manifiesto':fila[16], 'manifiesto':fila[17], 'codigo_documento_transporte':fila[18], 'documento_transporte':fila[19],
                         'aduana':fila[20], 'pais_origen':fila[21], 'pais_procedencia':fila[22], 'pais_embarque':fila[23], 'puerto_embarque':fila[24],
                         'via_transporte':fila[25], 'contenedores':fila[26], 'deposito':fila[27], 'fob':fila[28], 'flete':fila[29],
                         'seguro':fila[30], 'cif':fila[31], 'base_imponible':fila[32], 'kgs_neto':fila[33], 'kgs_bruto':fila[34],
                         'unidades':fila[35], 'tipo_unidad':fila[36], 'cantidad_comercial':fila[37], 'unidad_comercial':fila[38], 'tipo_unidad_nomenclador':fila[39],
                         'precio_unitario':fila[40], 'adval':fila[41], 'moneda':fila[42], 'embarcador':fila[43], 'codigo_liberacion':fila[44],
                         'estado_mercaderia':fila[45], 'clase_mercaderia':fila[46], 'pais_destino':fila[47], 'total_fob':fila[48], 'total_flete':fila[49],
                         'total_seguro':fila[50], 'total_cif':fila[51], 'total_kgs_neto':fila[52], 'total_kgs_bruto':fila[53], 'total_base_imponible':fila[54],
                         'total_cantidad_bultos':fila[55], 'clase':fila[56], 'verificador':fila[57], 'agente_afianzado':fila[58], 'nave':fila[59],
                         'agencia_transporte':fila[60], 'empresa_transporte':fila[61], 'aforador':fila[62], 'fecha_aforo':fila[63], 'tipo_aforo':fila[64],
                         'direccion_consignatario':fila[65], 'estado':fila[66], 'caracteristica':fila[67], 'unidad_medida':fila[68], 'caracteristica_agregada':fila[69],
                         'ranking_import':fila[70], 'modelo_homologado':fila[71]}
            importaciones.append(importacion)
        return importaciones
    

@blp.route("/consulta-top-marcas-unidades")
#
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "WHERE "  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
        print(where_clause)
        importaciones=[]
        print("""select NOMBRE_MARCA,sum(UNIDADES) from bd_importacion.importacion 
                       join bd_importacion.marcas on importacion.id_marca=marcas.id_marca
                       join bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
                               {0} 
                               group by NOMBRE_MARCA order by sum(UNIDADES) DESC LIMIT 10
                               """.format(where_clause))
        cursor=obtener_conexion().cursor()
        cursor.execute("""select NOMBRE_MARCA,sum(UNIDADES) from bd_importacion.importacion 
                       join bd_importacion.marcas on importacion.id_marca=marcas.id_marca
                       join bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
                               {0} 
                               group by NOMBRE_MARCA order by sum(UNIDADES) DESC LIMIT 10
                               """.format(where_clause))
        result=cursor.fetchall()
        
        cursor.close()
        for fila in result:
            importacion={
                         'nombre_marca':fila[0], 'unidades':fila[1]}
            importaciones.append(importacion)
        return jsonify(importaciones)

@blp.route("/consulta-top-marcas-fob")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "WHERE "  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))


        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""select NOMBRE_MARCA,sum(FOB) from bd_importacion.importacion join 
                       bd_importacion.marcas on importacion.id_marca=marcas.id_marca
                       join bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
                               {0} 
                               group by NOMBRE_MARCA order by sum(FOB) DESC LIMIT 10
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'nombre_marca':fila[0], 'fob':fila[1]}
            importaciones.append(importacion)
        return importaciones
    
@blp.route("/consulta-importaciones-fob-unidades")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = ""  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
       
        
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""select Year(Fecha_despacho) as Año,sum(FOB), sum(unidades) 
                       from bd_importacion.importacion 
                       join bd_importacion.marcas on importacion.id_marca=marcas.id_marca
                       join bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
                               WHERE  {0} 
                               group by Year(Fecha_despacho) order by Year(Fecha_despacho)
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'anio':fila[0], 'fob':fila[1], 'unidades':fila[2]}
            importaciones.append(importacion)
        return importaciones

@blp.route("/consulta-share-por-marcas")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = ""  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += "id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND Year(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND marcas.Nombre_Marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']])) 
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND categoria_importacion.subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
        
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    subconsulta.Año,
    subconsulta.Nombre_Marca,
    subconsulta.Total_fob,
    ROUND((subconsulta.Total_fob / total_por_año.total_fob_por_año) * 100, 2) AS Porcentaje
FROM
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            marcas.Nombre_Marca,
            SUM(importacion.fob) AS Total_fob
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            
            {0}
        GROUP BY 
            Year(importacion.Fecha_despacho), marcas.Nombre_Marca
    ) AS subconsulta
JOIN 
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            SUM(fob) AS total_fob_por_año
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            
            {0}
        GROUP BY 
            Year(Fecha_despacho)
    ) AS total_por_año ON subconsulta.Año = total_por_año.Año

ORDER BY 
    subconsulta.Año, subconsulta.Nombre_Marca;
                               """.format(where_clause))
        print("""SELECT 
    subconsulta.Año,
    subconsulta.Nombre_Marca,
    subconsulta.Total_fob,
    ROUND((subconsulta.Total_fob / total_por_año.total_fob_por_año) * 100, 2) AS Porcentaje
FROM
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            marcas.Nombre_Marca,
            SUM(importacion.fob) AS Total_fob
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            
            {0}
        GROUP BY 
            Year(importacion.Fecha_despacho), marcas.Nombre_Marca
    ) AS subconsulta
JOIN 
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            SUM(fob) AS total_fob_por_año
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            
            {0}
        GROUP BY 
            Year(Fecha_despacho)
    ) AS total_por_año ON subconsulta.Año = total_por_año.Año

ORDER BY 
    subconsulta.Año, subconsulta.Nombre_Marca;
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'anio':fila[0], 'nombre_marca':fila[1], 'fob':fila[2], 'porcentaje_fob':fila[3]}
            importaciones.append(importacion)
        return importaciones

@blp.route("/precio-promedio-por-marcas")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "" 
        if 'id_producto' in user_data:
            where_clause += "id_categoria_producto={0}".format(user_data['id_producto'])
        if 'id_producto' in user_data and isinstance(user_data['id_producto'], list) and len(user_data['id_producto']) > 0:
            where_clause += " AND id_categoria={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))        
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
    
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    Month(Fecha_despacho) AS Mes,
    Nombre_Marca,
    ROUND(SUM(FOB)/SUM(UNIDADES),2) AS Precio_Promedio
FROM 
    bd_importacion.importacion
JOIN 
    bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
JOIN 
    bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
WHERE 
    {0}
GROUP BY 
    Month(Fecha_despacho), Nombre_Marca
ORDER BY 
    Month(Fecha_despacho), Nombre_Marca; 

""".format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'mes':fila[0], 'nombre_marca':fila[1], 'precio_promedio':fila[2]}
            importaciones.append(importacion)
        return importaciones
    

@blp.route("/consulta-fob-por-importador")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = "WHERE "  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))        
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
                
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    i.razon_social,
    SUM(f.FOB) AS Suma_FOB,
    ROUND((SUM(f.FOB) / total_fob.suma_total_fob) * 100, 2) AS Porcentaje_FOB
FROM 
    bd_importacion.importacion f
JOIN 
    bd_importacion.importador i ON f.id_importador = i.id_importador
JOIN 
    bd_importacion.marcas ON f.id_marca = marcas.id_marca
JOIN 
    bd_importacion.categoria_importacion on f.id_subcategoria=categoria_importacion.id_subcategoria
JOIN (
    SELECT 
        id_importador,
        SUM(FOB) AS suma_total_fob
    FROM 
        bd_importacion.importacion
JOIN 
    bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
JOIN 
    bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
    {0}
    GROUP BY 
        id_importador
    ORDER BY 
        suma_total_fob DESC
    LIMIT 10
) AS top_10_importadores ON f.id_importador = top_10_importadores.id_importador
JOIN (
    SELECT 
        SUM(suma_total_fob) AS suma_total_fob
    FROM 
        (
            SELECT 
                id_importador,
                SUM(FOB) AS suma_total_fob
            FROM 
                bd_importacion.importacion
JOIN 
    bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
JOIN 
    bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
                       {0}
            GROUP BY 
                id_importador
            ORDER BY 
                suma_total_fob DESC
            LIMIT 10
        ) AS top_10_importadores
) AS total_fob
{0}
GROUP BY 
    i.razon_social, total_fob.suma_total_fob
ORDER BY 
    Porcentaje_FOB DESC;

                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'importador':fila[0], 'total_fob':fila[1], 'porcentaje_fob':fila[2]}
            importaciones.append(importacion)
        return importaciones


    
@blp.route("/consulta-share-por-segmento")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = ""  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " AND id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND Year(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND marcas.Nombre_Marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))        
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
                   
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    subconsulta.Año,
    subconsulta.CARACTERISTICA_AGREGADA,
    subconsulta.Total_fob,
    ROUND((subconsulta.Total_fob / total_por_año.total_fob_por_año) * 100, 2) AS Porcentaje
FROM
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            importacion.CARACTERISTICA_AGREGADA,
            SUM(importacion.fob) AS Total_fob
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            importacion.CARACTERISTICA_AGREGADA IS NOT NULL 
            {0}
        GROUP BY 
            Year(importacion.Fecha_despacho), importacion.CARACTERISTICA_AGREGADA
    ) AS subconsulta
JOIN 
    (
        SELECT 
            Year(Fecha_despacho) AS Año,
            SUM(fob) AS total_fob_por_año
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            CARACTERISTICA_AGREGADA IS NOT NULL
            {0}
        GROUP BY 
            Year(Fecha_despacho)
    ) AS total_por_año ON subconsulta.Año = total_por_año.Año

ORDER BY 
    subconsulta.Año, subconsulta.CARACTERISTICA_AGREGADA;
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            importacion={
                         'anio':fila[0], 'caracteristica':fila[1], 'fob':fila[2], 'porcentaje_fob':fila[3]}
            importaciones.append(importacion)
        return importaciones

@blp.route("/consulta-caracteristicas-por-marca")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = ""  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " AND id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND Year(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(importacion.Fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND marcas.Nombre_Marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))        
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
                 
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    t1.Marca,
    t1.Total_Unidades,
    t1.Total_FOB,
    t2.CARACTERISTICA_AGREGADA,
    t2.Unidades_por_caracteristica,
    t2.Fob_por_caracteristica
FROM
    (
        SELECT 
            marcas.nombre_marca AS Marca,
            SUM(importacion.UNIDADES) AS Total_Unidades,
            SUM(importacion.FOB) AS Total_FOB
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            importacion.CARACTERISTICA_AGREGADA IS NOT NULL 
                       {0}
        GROUP BY 
            marcas.nombre_marca
    ) t1
LEFT JOIN
    (
        SELECT 
            marcas.nombre_marca AS Marca,
            importacion.CARACTERISTICA_AGREGADA,
            SUM(importacion.UNIDADES) AS Unidades_por_caracteristica,
            SUM(importacion.fob) AS Fob_por_caracteristica
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
             importacion.CARACTERISTICA_AGREGADA IS NOT NULL
            {0}
        GROUP BY 
            marcas.nombre_marca, importacion.CARACTERISTICA_AGREGADA
    ) t2 ON t1.Marca = t2.Marca
ORDER BY 
    t1.Marca, t2.CARACTERISTICA_AGREGADA;
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        respuesta_final = {}
        caracteristicas_por_marca = []
        for fila in result:
            importacion = {
                'carcateristica': fila[3],
                'car_unidades': fila[4],
                'car_fob': fila[5]
            }
            if fila[0] not in respuesta_final:
                respuesta_final[fila[0]] = {
                    'marca': fila[0],
                    'total_fob': fila[2],
                    'total_unidades': fila[1],
                    'carcateristicas': []
            }
            respuesta_final[fila[0]]['carcateristicas'].append(importacion)
        return respuesta_final

@blp.route("/consulta-ventas-por-importador")
class Consulta_Imp(MethodView):
    @blp.arguments(ConsultaImpSch)
    @jwt_required()
    def post(self,user_data):  
        where_clause = ""  # '1' es siempre verdadero, lo que permite agregar condiciones de manera más fácil
        if 'id_producto' in user_data:
            where_clause += " AND id_categoria_producto={0}".format(user_data['id_producto'])
        if 'anio' in user_data and isinstance(user_data['anio'], list) and len(user_data['anio']) > 0:
            where_clause += " AND YEAR(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['anio'])))
        if 'mes' in user_data and isinstance(user_data['mes'], list) and len(user_data['mes']) > 0:
            where_clause += " AND MONTH(fecha_despacho) IN ({0})".format(", ".join(map(str, user_data['mes'])))
        if 'nombre_marca' in user_data and isinstance(user_data['nombre_marca'], list) and len(user_data['nombre_marca']) > 0:
            where_clause += " AND nombre_marca IN ({0})".format(", ".join(["'{0}'".format(marca) for marca in user_data['nombre_marca']]))
        if 'caracteristica' in user_data and isinstance(user_data['caracteristica'], list) and len(user_data['caracteristica']) > 0:
            where_clause += " AND caracteristica_agregada IN ({0})".format(", ".join(["'{0}'".format(caracteristica) for caracteristica in user_data['caracteristica']]))        
        if 'subcategoria' in user_data and isinstance(user_data['subcategoria'], list) and len(user_data['subcategoria']) > 0:
            where_clause += " AND subcategoria IN ({0})".format(", ".join(["'{0}'".format(subcategoria) for subcategoria in user_data['subcategoria']]))
          
        importaciones=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT 
    t1.Importador,
    t1.Total_Unidades,
    t1.Total_FOB,
    t2.Marca,
    t2.Unidades_por_marca,
    t2.Fob_por_marca
FROM
    (
        SELECT 
            importador.razon_social AS Importador,
            SUM(importacion.UNIDADES) AS Total_Unidades,
            SUM(importacion.FOB) AS Total_FOB
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.importador ON importacion.id_importador = importador.id_importador
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
            importacion.CARACTERISTICA_AGREGADA IS NOT NULL {0}
        GROUP BY 
            importador.razon_social
    ) t1
LEFT JOIN
    (
        SELECT 
            importador.razon_social AS Importador,
            marcas.nombre_marca AS Marca,
            SUM(importacion.UNIDADES) AS Unidades_por_marca,
            SUM(importacion.fob) AS Fob_por_marca
        FROM 
            bd_importacion.importacion
        JOIN 
            bd_importacion.importador ON importacion.id_importador = importador.id_importador
        JOIN 
            bd_importacion.marcas ON importacion.id_marca = marcas.id_marca
        JOIN 
            bd_importacion.categoria_importacion on importacion.id_subcategoria=categoria_importacion.id_subcategoria
        WHERE 
             importacion.CARACTERISTICA_AGREGADA IS NOT NULL {0}
        GROUP BY 
            importador.razon_social, marcas.nombre_marca
    ) t2 ON t1.Importador = t2.Importador
ORDER BY 
    t1.Importador, t2.Marca;
                               """.format(where_clause))
        result=cursor.fetchall()
        cursor.close()
        respuesta_final = {}
        for fila in result:
            importacion = {
                'marca': fila[3],
                'mar_unidades': fila[4],
                'mar_fob': fila[5]
            }
            if fila[0] not in respuesta_final:
                respuesta_final[fila[0]] = {
                    'importador': fila[0],
                    'total_fob': fila[2],
                    'total_unidades': fila[1],
                    'marcas': []
            }
            respuesta_final[fila[0]]['marcas'].append(importacion)
        return respuesta_final
    
@blp.route("/consulta-anios-fecha-despacho/<int:id>")
class AniosDespacho(MethodView):
    @jwt_required()
    def get(self,id):
        anios=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT DISTINCT YEAR(fecha_despacho) AS anio FROM bd_importacion.importacion 
                       WHERE  id_categoria_producto={0}
                        ORDER BY anio ASC;""".format(id))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            anio={'anio':fila[0]}
            anios.append(anio)
        return anios
    
@blp.route("/consulta-filtro-caracteristicas/<int:id>")
class AniosDespacho(MethodView):
    @jwt_required()
    def get(self,id):
        carcateristicas=[]
        cursor=obtener_conexion().cursor()
        cursor.execute("""SELECT DISTINCT CARACTERISTICA_AGREGADA  FROM bd_importacion.importacion 
                       WHERE CARACTERISTICA_AGREGADA IS NOT NULL and id_categoria_producto={0};""".format(id))
        result=cursor.fetchall()
        cursor.close()
        for fila in result:
            carcateristica={'caracteristica':fila[0]}
            carcateristicas.append(carcateristica)
        return carcateristicas