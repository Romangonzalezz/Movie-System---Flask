import json

with open ("prueba_logica/usuarios.json","r") as archivojson:
    usuarios = json.load(archivojson)

with open ("prueba_logica/peliculas.json", "r") as peliculas_json:
     peliculas= json.load(peliculas_json)

with open ("prueba_logica/comentarios.json","r", ) as comentarios_json:
    comentarios = json.load(comentarios_json)

# def guardar_json():
#     with open ("prueba_logica/peliculas_prueba.json", "w") as peliculas_json:
#         json.dump(peliculas, peliculas_json, ident=6)



def MenuBienvenida():
    opcion = 0
    while not(opcion>=1 and opcion<=3):        
        print("1) Iniciar sesion")
        print("2) Ingresar como invitado")
        opcion = int(input("Ingresar opcion: "))
    return opcion

def IniciarSesion():
    #system("cls")
    while True:        
        usuarioIngresado = input("Ingrese su usuario: ").lower()
        contrasenaIngresada =  input("Ingrese su contraseña: ").lower()        
        for usuario in usuarios:
            if usuario["nombre"] == usuarioIngresado and usuario["password"] == contrasenaIngresada:
                input("Bienvenido!! Precione enter para continuar!")
                return usuario["id"]

def Comentarios():
    opcion = 0
    while not(opcion>=1 and opcion<=4):        
        print("1) Agregar un comentario.")
        print("2) Eliminar un comentario.")
        print("3) Editar un comentario.")
        opcion = int(input("Ingrese opcion: "))
    return opcion

def agregarComentario(idUsuario):
    
    agregar = input("Ingrese ID o Nombre de la pelicula: ")
    for pelicula in peliculas:
        if """pelicula["id"] == agregar or""" or pelicula["titulo"].lower() == agregar:            
            comentario = input("¿Que comentario quiere agregar?: ")
            idComentarioNuevo = int(comentarios[-1]["id"]) + 1
            nuevoComentario={"id":str(idComentarioNuevo),"idUsuario":idUsuario,"comentario":comentario}            
            comentarios.append(nuevoComentario)   

        print("Comentario exitoso!!")
        with open("prueba_logica/peliculas.json", "w") as comentarios_json:        
            json.dump(peliculas, comentarios_json, indent=4)
        with open("prueba_logica/comentarios.json", "w") as comentarios_json:        
            json.dump(comentarios, comentarios_json, indent=4)
        input("Ingrese enter para continuar...")
        return MenuBienvenida()


def eliminarComentario(idUsuario):
    listaComentariosUsuario = []
    encontrada = False
    #Lista de comentarios
    print("Su lista de comentarios es: ")
    print("=====================")
    for comentario in comentarios:
        if comentario["idUsuario"] == idUsuario:
            listaComentariosUsuario.append(comentario["id"])
            print("ID=",comentario["id"],"\nComentario:",comentario["comentario"])
            print("=====================")
    
    #Validacion de entrada
    while True:
        borrar = input("Ingrese el ID del comentario que desea eliminar: ")
        if borrar in listaComentariosUsuario:
            encontrada = True
            break
        else:
            print("Error, ingreso un numero que no es suyo o no existe")
    
    for comentario in comentarios:
        if comentario["id"] == borrar:
            comentarios.remove(comentario)

    for pelicula in peliculas:
        for comentarioRecorrido in pelicula["comentarios"]:
            if comentarioRecorrido == borrar:
                pelicula["comentarios"].remove(comentarioRecorrido)
                
    #comentario de salida + guardado de jsons
    if encontrada == True:
        print("Borrado con exito")
        with open("peliculas.json", "w") as comentarios_json:
        
            json.dump(peliculas, comentarios_json, indent=4)
        with open("prueba_logica/comentarios.json", "w") as comentarios_json:
            json.dump(comentarios, comentarios_json, indent=4)
    else:
        print("Error al borrar")
    input("Ingrese enter para continuar...")
    return MenuBienvenida()
    
def modificarComentario(idUsuario):
    listaComentariosUsuario = []
    encontrada = False
    #Lista de comentarios by idUsuario
    print("Su lista de comentarios es: ")
    print("=====================")
    for comentario in comentarios:
        if comentario["idUsuario"] == idUsuario:
            listaComentariosUsuario.append(comentario["id"])
            print("ID=",comentario["id"],"\nComentario:",comentario["comentario"])
            print("=====================")
    
    #Validacion de entrada
    while True:
        modificar = input("Ingrese el ID del comentario que desea modificar: ")
        if modificar in listaComentariosUsuario:
            encontrada = True
            break
        else:
            print("Error, ingreso un numero que no es suyo o no existe")

    while True:
        comentarioNuevo = input("Ponga su mensaje modificado:\n")
        if comentarioNuevo != "":
            break

    for comentario in comentarios:
        if comentario["id"] == modificar:
            comentario["comentario"] = comentarioNuevo

    if encontrada == True:
        print("Modificacion con exito")
        with open("prueba_logica/peliculas.json", "w") as comentarios_json:
            json.dump(peliculas, comentarios_json, indent=4)
        with open("prueba_logica/comentarios.json", "w") as comentarios_json:
            json.dump(comentarios, comentarios_json, indent=4)
    else:
        print("Error al modificar")
    input("Ingrese enter para continuar...")
    return MenuBienvenida()


def funcion_main_prueba():
    opcionMenu= 0
    while opcionMenu != 3:
        opcionMenu= MenuBienvenida()
        #Menu 1 y 2 cargar o no cargar usuario
        if opcionMenu == 1:
            idUsuario = IniciarSesion()
            opcionComentario= Comentarios()
            if opcionComentario == 1:
                agregarComentario(idUsuario)
            elif opcionComentario == 2:
                eliminarComentario(idUsuario)
            else:
                modificarComentario(idUsuario)
        # if nocargarusuario == 2:
        #     ultimas10pelis()

funcion_main_prueba()