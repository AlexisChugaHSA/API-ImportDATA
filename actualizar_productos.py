import logging
from bd import obtener_conexion
import datetime

logging.basicConfig(level=logging.INFO)

def actualizar_productos():
    logging.info("Iniciando el proceso de actualización de productos")
    fecha_actual = datetime.datetime.now().date()
    logging.info(f"Fecha actual: {fecha_actual}")
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query_select = """SELECT id_producto_usuario, fecha_hasta FROM producto_usuario 
    WHERE fecha_hasta < %s AND activo = 1 """
    cursor.execute(query_select, (fecha_actual,))
    registros = cursor.fetchall()
    logging.info(f"Registros encontrados para actualizar: {len(registros)}")
    if registros:
        query_update = """UPDATE producto_usuario SET activo = 0 WHERE id_producto_usuario = %s"""
        for registro in registros:
            cursor.execute(query_update, (registro[0],))
            logging.info(f"Actualizado registro con id: {registro[0]}")
        conexion.commit()
        logging.info("Actualización completada y cambios confirmados.")
    cursor.close()
    conexion.close()
    logging.info("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    actualizar_productos()
