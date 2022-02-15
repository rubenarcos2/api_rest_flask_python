from flask import Flask, render_template, request, redirect
import app.controlador_usuarios

app = Flask(__name__)

@app.route("/agregar_usuario")
def formulario_agregar_usuario():
    return render_template("agregar_usuario.html")


@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    usuario_github = request.form["usuario_github"]
    controlador_usuarios.insertar_usuario(nombre, direccion, telefono, email, usuario_github)
    controlador_usuarios.get_repo_usuario_github(usuario_github) #Se obtienen los repos y se insertan en la tabla
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/usuarios")


@app.route("/")
@app.route("/usuarios")
def usuarios():
    usuarios = controlador_usuarios.obtener_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/repositorios/<string:usuario_github>")
def repositorios(usuario_github):
    repos = controlador_usuarios.obtener_repositorio_usuario(usuario_github)
    if repos != None:
        return render_template("repositorios.html", repositorios=repos, usuario_github=usuario_github)
    else:
        return render_template("repositorios.html", msg="No hay repositorios para el usuario")


@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controlador_usuarios.eliminar_usuario(request.form["id"])
    return redirect("/usuarios")


@app.route("/formulario_editar_usuario/<int:id>")
def editar_usuario(id):
    # Obtener el usuario por ID
    usuario = controlador_usuarios.obtener_usuario_por_id(id)
    return render_template("editar_usuario.html", usuario=usuario)


@app.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    id = request.form["id"]
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    usuario_github = request.form["usuario_github"]
    controlador_usuarios.actualizar_usuario(nombre, direccion, telefono, email, usuario_github, id)
    return redirect("/usuarios")


# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
