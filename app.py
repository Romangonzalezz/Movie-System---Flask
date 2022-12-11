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

# Listar Usuarios Postman
@app.route('/usuarios')
def ListaUsuarios():
    return(usuarios)


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


# Listar Peliculas Postman
@app.route('/peliculas')
def ListarPeliculas():
    return peliculas

# Agregar peliculas
@app.route("/agregar/pelicula", methods = ["POST"])
def agregar_pelicula():
    #Abrimos Json metodo Write
    with open ('peliculas.json', "w") as peliculas_file:
        json.dump(peliculas, peliculas_file,indent=5)

    #Recibir datos del clientes
    data = request.get_json()
    temp = peliculas["peliculas"]

    # Chequeamos si esta bien el body de POSTMAN
    if ("titulo" in data) and ("anio" in data) and ("director" in data) and ("genero" in data) and ("sipnosis" in data) and ("imagen" in data):
        temp.append(data)
        return Response('Agregada exitosamente ' + data["titulo"], status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)

# Eliminar peliculas
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
    
    
''' 
# Actualizar pelicula
@app.route("/actualizar/pelicula", methods = ["PUT"])
def actualizar_datos_pelicula():
    data = request.get_json()
    if (("titulo" in data) and ("anio" in data) and ("genero" in data)):
        for pelicula in peliculas["peliculas"]:
            if ((pelicula["titulo"] == data["titulo"]) and (pelicula["anio"] == data["anio"]) and (pelicula["genero"] in data["genero"])):            
                print("pelicula actualizada")
                return Response(status= HTTPStatus.OK)
    else:
        return Response("{}", status= HTTPStatus.BAD_REQUEST)
'''



if __name__ == '__main__':
    app.run(debug=True)