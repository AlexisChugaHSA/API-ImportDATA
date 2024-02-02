import pymysql

def obtener_conexion():
    return pymysql.connect(host='170.239.154.79',user='HSAMSQL_',password='serverHSA**PricingImport',db='bd_import_pricing', port=3306)