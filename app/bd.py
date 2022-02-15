import pymysql


def obtener_conexion():
    try:
        # return pymysql.connect(host='localhost',
        #                         user='root',
        #                         password='',
        #                         db='repositorios')
        return pymysql.connect(
                           host='db4free.net',
                           user='sbd_tarea_24',
                           password='sbd_tarea_2-4123456',
                           db='sbd_tarea_24')
    except pymysql.err.InternalError as e:
        print("Error interno del servidor", e)
        raise e
    except pymysql.err.DatabaseError as e:
        print("No se puede conectar al servidor", e)
        raise e
    except Exception as e:
        print("ERROR:", e)
        raise e