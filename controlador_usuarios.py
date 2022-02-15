from bd import obtener_conexion
import requests
from json.decoder import JSONDecodeError
import json

def insertar_usuario(nombre, direccion, telefono, email, usuario_github):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombre, direccion, telefono, email, usuario_github) VALUES (%s, %s, %s, %s, %s)", (nombre, direccion, telefono, email, usuario_github))
    conexion.commit()
    conexion.close()

def insertar_repositorio(id, name, html_url, description, created_at, usuario_github):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO repositorios(id, name, html_url, description, created_at, usuario_github) VALUES (%s, %s, %s, %s, %s, %s)", (id, name, html_url, description, created_at, usuario_github))
    conexion.commit()
    conexion.close()

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, direccion, telefono, email, usuario_github FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, direccion, telefono, email, usuario_github FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario


def actualizar_usuario(nombre, direccion, telefono, email, usuario_github, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre = %s, direccion = %s, telefono = %s, email = %s, usuario_github = %s WHERE id = %s",
                       (nombre, direccion, telefono, email, usuario_github, id))
    conexion.commit()
    conexion.close()
    eliminar_repo_usuario_github(usuario_github)
    get_repo_usuario_github(usuario_github)


def get_repo_usuario_github(usuario):
    params = {'sort': 'updated'}
    response = requests.get("https://api.github.com/users/" + usuario + "/repos", params=params)
    response.raise_for_status()
    github_resp = json.loads(response.text)
    if len(github_resp) > 0:
        for repo in github_resp:
            insertar_repositorio(repo['id'], repo['name'], repo['html_url'], repo['description'], repo['created_at'], usuario)
    else:
        print("No existe el usuario indicado")


def obtener_repositorio_usuario(usuario_github):
    conexion = obtener_conexion()
    repositorio = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, html_url, description, created_at, usuario_github FROM repositorios WHERE usuario_github = %s", (usuario_github,))
        repositorio = cursor.fetchall()
    conexion.close()
    return repositorio


def eliminar_repo_usuario_github(usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM repositorios WHERE usuario_github = %s", (usuario,))
    conexion.commit()
    conexion.close()