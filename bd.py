import pymysql


def obtener_conexion():
    try:
        return pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='repositorios')
    except pymysql.err.InternalError as e:
        print("Error interno del servidor", e)
        raise e
    except pymysql.err.DatabaseError as e:
        print("No se puede conectar al servidor", e)
        raise e
    except Exception as e:
        print("ERROR:", e)
        raise e
