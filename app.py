import flask, json
from flask import Flask, Response, request, render_template, redirect, jsonify
from http import HTTPStatus

app = Flask(__name__)

#Cargamos los JSON en nuestro Core
with open ("usuarios.json", encoding='utf-8') as usuarios_json:
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

# Listar Usuarios
@app.route('/usuarios')
def ListaUsuarios():
    return(usuarios)

# Cuando el usuario esta logeado
@app.route('/usuario_premium')
def UsuarioPremium():
    return render_template('autorizado.html', usuarios=usuarios, peliculas=peliculas)

# Listar Peliculas POSTMAN
@app.route('/peliculas')
def ListarPeliculas():
    return peliculas

# Agregar peliculas desde POSTMAN
@app.route("/agregar/pelicula", methods = ["POST"])
def agregar_pelicula():
    #Abrimos Json metodo Write
    with open ('peliculas.json', "w") as peliculas_file:
        json.dump(peliculas, peliculas_file,indent=5)

    #Recibir datos del clientes
    data = request.get_json()
    temp = peliculas["peliculas"]

    #Si lo hacemos con el Get como generamos un id automatico antes y lo importamos a DATA 
    # antes de subir a PELICULAS. Porque lo mismo nos va a pasar en comentarios.
    # id_pelicula= pelicula["peliculas"][-1]["id"]
    # id= id_pelicula

    # Chequeamos si esta bien el body de POSTMAN
    if ("titulo" in data) and ("anio" in data) and ("director" in data) and ("genero" in data) and ("sinopsis" in data) and ("imagen" in data):
        temp.append(data)
        return Response('Agregada exitosamente ' + data["titulo"], status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)

# Eliminar peliculas con el Titulo y Anio desde POSTMAN
@app.route('/peliculas/delete', methods=['DELETE'])
def eliminar_pelicula():
    #Recibimos data del POSTMAN
    data = request.get_json()
    
    #Chequeamos la data
    if request.method == 'DELETE':
        for pelicula in peliculas["peliculas"]:
            if ("titulo" in data) and ("anio" in data):
                if (pelicula["titulo"] == data["titulo"]) and (pelicula["anio"] == data["anio"]):
                    
                    print("estamos aca")

                    # Borramos la pelicula del JSON
                    pelicula.clear()
    
                    # Dumpeamos Json en modoo Write
                    with open ('peliculas.json', "w") as peliculas_file:
                        json.dump(peliculas, peliculas_file, indent=5)

                    return Response('Pelicula borrada exitosamente', status= HTTPStatus.OK)
        else:
            return Response("{}", status= HTTPStatus.BAD_REQUEST)
    

# Actualizar pelicula
@app.route("/actualizar/pelicula", methods = ["PUT"])
def actualizar_datos_pelicula():

    # Recibimos data del body POSTMAN, (la pelicula que vamos a modificar)
    data = request.get_json()
    

    # Chequeamos si es por el metodo http PUT
    if request.method == 'PUT':
        for pelicula in peliculas["peliculas"]:
            if ("titulo" in data):
                if (pelicula["titulo"] == data["titulo"]):
                    print(pelicula)
                    if ("titulo" in data) or ("anio" in data) or ("director" in data) or ("genero" in data) or ("sinopsis" in data) or ("imagen" in data):
                            if ("anio" in data):    
                                pelicula["anio"] = data["anio"]
                            if ("director" in data):  
                                pelicula["director"] = data["director"]
                            if ("genero" in data):
                                pelicula["genero"] = data["genero"]
                            if ("sinopsis" in data):
                                pelicula["sinopsis"] = data["sinopsis"]
                            if ("imagen" in data):
                                pelicula["imagen"] = data["imagen"]

                    #Dumpeamos en el JSON
                    with open ('peliculas.json', "w") as peliculas_file:
                        json.dump(peliculas, peliculas_file, indent=5)

                    # MOSTRAMOS EN EL POSTMAN LOS CAMPOS DE LA PELICULA CON SUS DATOS
                    return Response("Pelicula modificada",status= HTTPStatus.OK)
                    
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)


# Forms desde HTML 

# Ingresar Usuario desde Formulario HTML
@app.route('/login', methods=['GET', 'POST'])
def Ingresar():
    user = request.form.get('user')
    passw = request.form.get('password')
    if request.method == 'POST':
        for usuario in usuarios['usuarios']:
            if (usuario['nombre'] == user) and (usuario['password'] == passw):
                return redirect('/usuario_premium')
            else:
                return('Error cuenta no registrada o campos incorrectos')
    return render_template('login.html', usuarios=usuarios)

# Agregar peliculas desde HTML
@app.route("/usuario_premium", methods = ["POST"])
def agregar_pelicula_html():
    #Recibir datos del clientes
    data_titulo = request.form.get('titulo')
    data_anio = request.form.get('anio')
    data_director = request.form.get('director')
    data_genero = request.form.get('genero')
    data_sinopsis = request.form.get('sinopsis')
    data_imagen = request.form.get('imagen')

    temp = peliculas["peliculas"]
    # Validamos informacion del formulario
    if request.method == 'POST':
            json_html = {
                "titulo": data_titulo,
                "anio": data_anio,
                "director": data_director,
                "genero": data_genero,
                "sinopsis": data_sinopsis,
                "imagen": data_imagen
            }

            jsonify(json_html)
            
            # Pasamos la info al JSON
            temp.append(json_html)

            #Abrimos Json metodo Write
            with open ('peliculas.json', "w") as peliculas_file:
                json.dump(peliculas, peliculas_file, indent=5)
            return Response('Pelicula agregada exitosamente ', status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)


# Eliminar peliculas desde HTML
@app.route("/usuario_premium/eliminar_pelicula", methods = ["GET","POST"])
def eliminar_pelicula_html():

    #Recibimos data del FORMULARIO HTML
    data = request.form.get('titulo')
    
    #Chequeamos la data
    if request.method == 'POST':
        for pelicula in peliculas["peliculas"]:
                if (data == pelicula["titulo"]):
                
                    # Borramos la pelicula del JSON
                    pelicula.clear()

                    # Dumpeamos Json en modoo Write
                    with open ('peliculas.json', "w") as peliculas_file:
                        json.dump(peliculas, peliculas_file, indent=5)

                    return Response('Pelicula borrada exitosamente', status= HTTPStatus.OK)
        else:
            return Response("{}", status= HTTPStatus.BAD_REQUEST)
    return render_template('eliminar_pelicula.html', peliculas=peliculas)


if __name__ == '__main__':
    app.run(debug=True)
