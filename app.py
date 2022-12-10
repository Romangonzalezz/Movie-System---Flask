import flask, json
from flask import Flask, Response, request, render_template, redirect, jsonify
from http import HTTPStatus

app = Flask(__name__)


usuarios= []
with open ("usuarios.json", "r", encoding='utf-8') as usuarios_json:
    usuarios = json.load(usuarios_json)


with open ("peliculas.json", encoding='utf-8') as peliculas_json:
    peliculas = json.load(peliculas_json)

#Cantidad de Peliculas cargadas:
print("Peliculas: ", len(peliculas["peliculas"]))
 

# Home PAGINA PRINCIPAL HTML
@app.route('/Home')
@app.route('/')
def Home():
    return render_template('index.html', peliculas=peliculas)

# Listar Usuarios Postman
@app.route('/usuarios')
def ListaUsuarios():
    return jsonify(usuarios)


# Ingresar Usuario desde Formulario HTML
@app.route('/login', methods=['GET', 'POST'])
def Ingresar():
    user = request.form.get('user')
    passw = request.form.get('password')
    if request.method == 'POST':
        for usuario in usuarios['usuarios']:
            if (usuario['nombre'] == user) and (usuario['password'] == passw):
                return redirect('autorizado.html')
            else:
                return('Error cuenta no registrada o campos incorrectos')
    return render_template('login.html', usuarios=usuarios)

# Postman
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    global usuarios
    #Datos del index
    datos_usuario= request.get_json(usuarios_json)
    print(datos_usuario) 
    id_usuario= usuarios["usuarios"][-1]["id"]
    id= id_usuario+1
    if (("nombre" in datos_usuario) and ("password" in datos_usuario)):
        usuarios["usuarios"].append({
            "id": id,
            "nombre": datos_usuario["nombre"],
            "password": datos_usuario["password"]
            })
        #usuarios.insert
        return Response(status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)




'''
# Peliculas
@app.route('/peliculas')
def ListarPeliculas():
    return peliculas
# Agregar peliculas
@app.route("/agregar/pelicula", method = ["POST"])
def agregar_pelicula():
    #Recibir datos del cliente
    datos_cliente = request.get_json()
    #id?
    if (("titulo" in datos_cliente) and ("anio" in datos_cliente) and ("director" in datos_cliente) and ("genero" in datos_cliente) and ("actores" in datos_cliente) and ("sipnosis" in datos_cliente) and ("imagen" in datos_cliente)):
        peliculas["peliculas"].append({
            "titulo" : datos_cliente["titulo"],
            "anio" : datos_cliente["anio"],
            "director" : datos_cliente["director"],
            "genero" : datos_cliente["genero"],
            "actores": datos_cliente["actores"],
            "sipnosis" : datos_cliente["sipnosis"],
            "imagen" : datos_cliente["imagen"]
            })
        return Response(datos_cliente["titulo"], status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)
 
# Eliminar peliculas
@app.route('/peliculas/delete', methods=['DELETE'])
def eliminar_pelicula():
    datos_pelicula= request.get_json()
    if (["titulo"] in datos_pelicula) and (["anio"] in datos_pelicula)):
        #for pelicula in peliculas["titulo"]:
        print("pelicula borrada")
       return Response(datos_cliente["titulo"], status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)
        
    
# Actualizar pelicula
@app.route("/actualizar/pelicula", methods = ["PUT"])
def actualizar_datos_pelicula():
    datos_cliente = request.get_json()
    if (("titulo" in datos_cliente) and ("anio" in datos_cliente) and ("genero" in datos_cliente)):
        for pelicula in peliculas["peliculas"]:
            if ((pelicula["titulo"] == datos_cliente["titulo"]) and (pelicula["anio"] == datos_cliente["anio"]) and (pelicula["genero"] in datos_cliente["genero"])):            
                print("pelicula actualizada")
                return Response(status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)
'''


if __name__ == '__main__':
    app.run(debug=True)