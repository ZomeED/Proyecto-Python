import json

""" 
Proyecto: The Tower - Minijuego de rol
Gestión de personajes con guardado en fichero (Forma manual).
"""

ARCHIVO = "datos_heroes.json"

def cargar_datos():
    """ 
    Leer el fichero como texto y convertir a lista 
    """
    try:
        fichero = open(ARCHIVO, "r")
        
        contenido_texto = fichero.read()
        
        fichero.close()

        # Convertir la cadena JSON a un diccionario Python
        datos_json = json.loads(contenido_texto)
        
        print("--> Datos cargados correctamente.")
        return datos_json

    except:
        # Si hay error (ej. el fichero no existe aún), se devuelva la lista vacía
        return []

def guardar_datos(lista):
    """ 
    Convertir la lista a texto y escribirla en el fichero
    """
    # La función dumps() toma el objeto y devuelve un String
    # Usamos indent=4 para que sea legible
    texto_json = json.dumps(lista, indent=4)
    
    # Abrir el fichero en modo escritura , guardar la cadena de texto y cerrar para guardar los cambios
    fichero = open(ARCHIVO, "w")
    
    fichero.write(texto_json)
    
    fichero.close()


# --- INICIO DEL PROGRAMA ---

# Al arrancar, se intenta cargar lo que haya guardado
lista_heroes = cargar_datos()

def insertar_heroe(lista):
    """ Función para registrar un nuevo personaje """
    print("\n--- CREACIÓN DE PERSONAJE ---")
    
    nombre = input("Introduce el nombre de tu héroe: ")
    es_valido = True 
    
    if len(nombre) == 0:
        print("Error: El nombre no puede estar en blanco.")
        es_valido = False

    if es_valido:
        indice = 0
        while indice < len(lista) and es_valido:
            if lista[indice]['nombre'] == nombre:
                print("Error: Ya existe un héroe con este nombre.")
                es_valido = False
            indice += 1

    if es_valido:
        print("\n Clases disponibles:")
        print("1. Humano (Equilibrado)")
        print("2. Tanque (Mucho aguante, lento)")
        print("3. Duende (Muy rápido)")

        try:
            opcion = int(input("Elige una clase (1-3): "))
            
            clase = ""
            vida = 0
            ataque = 0
            velocidad = 0
            datos_correctos = False

            if opcion == 1:
                clase = "Humano"
                vida = 60
                ataque = 15
                velocidad = 20
                datos_correctos = True
            elif opcion == 2:
                clase = "Tanque"
                vida = 70
                ataque = 20
                velocidad = 10
                datos_correctos = True
            elif opcion == 3:
                clase = "Duende"
                vida = 50
                ataque = 15
                velocidad = 30
                datos_correctos = True
            else:
                print("Opción incorrecta. Tienes que poner 1, 2 o 3.")

            if datos_correctos:
                nuevo_heroe = {
                    "nombre": nombre,
                    "clase": clase,
                    "vida": vida,
                    "ataque": ataque,
                    "velocidad": velocidad
                }
                lista.append(nuevo_heroe)
                
                # GUARDAR: Actualizar el fichero cada vez que se cambia algo
                guardar_datos(lista)
                
                print("--> ¡Personaje creado! " + nombre + " es un " + clase + ".")

        except ValueError:
            print("Error: Debes introducir un número entero.")


def buscar_heroe(lista):
    """ Buscar un héroe por el nombre para imprimir sus datos """
    nombre_buscado = input("\nIntroduce nombre de héroe para buscar: ")
    encontrado = False
    i = 0
    
    while i < len(lista) and not encontrado:
        h = lista[i]
        if h["nombre"].lower() == nombre_buscado.lower():
            print("\n--- FICHA DEL HÉROE ---")
            print("Nombre: " + h['nombre'])
            print("Clase:  " + h['clase'])
            print("Vida:   " + str(h['vida']))
            print("Ataque: " + str(h['ataque']))
            encontrado = True
        i += 1
            
    if not encontrado:
        print("No se ha encontrado a nadie con ese nombre.")


def modificar_heroe(lista):
    """ Buscar un héroe para cambiarle el nombre """
    busqueda = input("\n¿Qué héroe quieres modificar?: ")
    encontrado = False
    i = 0
    
    while i < len(lista) and not encontrado:
        h = lista[i]
        if h["nombre"].lower() == busqueda.lower():
            print("Se va a modificar a: " + h['nombre'])
            nuevo_nombre = input("Introduce el nuevo nombre: ")
            
            if len(nuevo_nombre) > 0:
                h["nombre"] = nuevo_nombre
                
                # LLamar a la función que guarda los datos
                guardar_datos(lista)
                
                print("Nombre cambiado correctamente.")
            else:
                print("Error: No puedes dejar el nombre vacío.")
            
            encontrado = True
        i += 1

    if not encontrado:
        print("No encuentro a ese héroe en la lista.")


def eliminar_heroe(lista):
    """ Eliminar un personaje de la lista pidiendo confirmación """
    nombre = input("\n¿Qué héroe quieres eliminar?: ")
    encontrado = False
    i = 0
    
    while i < len(lista) and not encontrado:
        h = lista[i]
        if h["nombre"].lower() == nombre.lower():
            respuesta = input("¿Seguro que quieres borrar a " + h['nombre'] + "? (s/n): ")
            
            if respuesta.lower() == 's':
                del lista[i]
                
                # LLamar a la función que guarda los datos
                guardar_datos(lista)
                
                print("Héroe eliminado definitivamente.")
            else:
                print("Operación cancelada.")
            
            encontrado = True
        i += 1
            
    if not encontrado:
        print("No se puede borrar porque no existe ese héroe.")


def mostrar_todos(lista):
    """ Muestra un listado de todos los personajes registrados """
    print("\n--- LISTA DE PERSONAJES ---")
    
    if len(lista) == 0:
        print("Actualmente no hay héroes creados.")
    else:
        print(f"{'NOMBRE':<20} {'CLASE':<15} {'VIDA':<10}")
        print("-" * 45)

        for h in lista:
            print(f"{h['nombre']:<20} {h['clase']:<15} {h['vida']:<10}")

    print("-" * 45)


def menu():
    """ Función principal que contiene el menú de opciones """
    continuar = True
    
    while continuar:
        print("\n=== GESTIÓN DE HÉROES RPG ===")
        print("1. Crear Héroe")
        print("2. Buscar Héroe")
        print("3. Modificar Héroe")
        print("4. Eliminar Héroe")
        print("5. Ver Todos")
        print("6. Salir")
        
        opcion = input("Elige una opción: ")

        if opcion == "1":
            insertar_heroe(lista_heroes)
        elif opcion == "2":
            buscar_heroe(lista_heroes)
        elif opcion == "3":
            modificar_heroe(lista_heroes)
        elif opcion == "4":
            eliminar_heroe(lista_heroes)
        elif opcion == "5":
            mostrar_todos(lista_heroes)
        elif opcion == "6":
            print("Programa cerrado.")
            continuar = False
        else:
            print("Esa opción no existe, prueba otra vez.")

# Ejecutar el menú del programa
menu()