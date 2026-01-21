import json
import logging

""" 
Proyecto: The Tower - Minijuego de rol
Gestión de personajes con JSON y sistema de Logging según apuntes.
"""

ARCHIVO_JSON = "datos_heroes.json"
ARCHIVO_LOG = "registro_partida.log"

# --- 1. CONFIGURACIÓN DEL SISTEMA DE REGISTRO (Logging) ---

# El 'logger' raíz (root) se usa aquí para la configuración global.
logging.basicConfig(
    # 1. Nivel mínimo global: Se procesarán mensajes desde INFO
    level=logging.INFO, 
    
    # 2. Formato de los mensajes
    format='%(asctime)s - %(levelname)s - Módulo: %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    
    # 3. Handler 1: Guardar todos los mensajes (INFO+) en un fichero
    filename=ARCHIVO_LOG,
    # Modo 'a' (append) para añadir al final sin borrar lo anterior
    filemode='a'
)

def cargar_datos():
    """ 
    Lee el fichero JSON. Registra éxito o error en el log.
    """
    try:
        fichero = open(ARCHIVO_JSON, "r")
        contenido_texto = fichero.read()
        fichero.close()

        datos_recuperados = json.loads(contenido_texto)
        
        # Mensaje INFO (nivel 20): Se registrará en el fichero, pero no en la consola.
        logging.info("Sistema: Datos cargados correctamente desde JSON.")
        return datos_recuperados

    except Exception as e:
        # Mensaje WARNING (nivel 30): Se registra en fichero
        # Algo inesperado (fichero no existe) pero el programa sigue
        # Uso warning porque es normal la primera vez que se juega
        logging.warning(f"Sistema: No se encontró fichero previo o está vacío. Se inicia lista nueva. Detalle: {e}")
        return []

def guardar_datos(lista):
    """ 
    Guarda los datos en JSON. 
    """
    try:
        texto_json = json.dumps(lista, indent=4)
        fichero = open(ARCHIVO_JSON, "w")
        fichero.write(texto_json)
        fichero.close()
        
        # Mensaje INFO (nivel 20): Se registrará en el fichero, pero no en la consola.
        logging.info("Sistema: Datos guardados exitosamente en fichero JSON.")
        
    except Exception as e:
        print(f"Error crítico al guardar: {e}")
        # Uso de exc_info=True para registrar la traza completa de la pila (traceback)
        logging.error(f"Error CRÍTICO guardando datos: {e}", exc_info=True)


# --- INICIO DEL PROGRAMA ---

lista_heroes = cargar_datos()

def insertar_heroe(lista):
    """ Función para registrar un nuevo personaje """
    print("\n--- CREACIÓN DE PERSONAJE ---")
    
    nombre = input("Introduce el nombre de tu héroe: ")
    es_valido = True 
    
    if len(nombre) == 0:
        print("Error: El nombre no puede estar en blanco.")
        # LOG WARNING: El usuario hizo algo incorrecto, pero no rompió el programa
        logging.warning("Creación fallida: El usuario intentó usar un nombre vacío.")
        es_valido = False

    if es_valido:
        indice = 0
        while indice < len(lista) and es_valido:
            if lista[indice]['nombre'] == nombre:
                print("Error: Ya existe un héroe con este nombre.")
                # LOG WARNING: Intento de duplicado
                logging.warning(f"Creación fallida: El nombre '{nombre}' ya existe.")
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
                logging.warning(f"Creación fallida: Opción de clase inválida ({opcion}).")

            if datos_correctos:
                nuevo_heroe = {
                    "nombre": nombre,
                    "clase": clase,
                    "vida": vida,
                    "ataque": ataque,
                    "velocidad": velocidad
                }
                lista.append(nuevo_heroe)
                guardar_datos(lista)
                
                print("--> ¡Personaje creado! " + nombre + " es un " + clase + ".")
                # LOG INFO: Éxito en la creación
                logging.info(f"Acción: Nuevo héroe creado -> {nombre} ({clase})")

        except ValueError as e:
            print("Error: Debes introducir un número entero.")
            # LOG ERROR con exc_info=True:
            logging.error("Error de usuario: Introdujo texto en lugar de número.", exc_info=True)


def buscar_heroe(lista):
    """ Buscar un héroe por el nombre """
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
            # LOG INFO: Dejar constancia de la consulta
            logging.info(f"Consulta: Se visualizaron datos de {h['nombre']}.")
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
                nombre_antiguo = h["nombre"]
                h["nombre"] = nuevo_nombre
                
                guardar_datos(lista)
                
                print("Nombre cambiado correctamente.")
                # LOG INFO: Registro del cambio
                logging.info(f"Modificación: '{nombre_antiguo}' cambió nombre a '{nuevo_nombre}'.")
            else:
                print("Error: No puedes dejar el nombre vacío.")
                logging.warning(f"Modificación fallida: intento de nombre vacío para {h['nombre']}.")
            
            encontrado = True
        i += 1

    if not encontrado:
        print("No encuentro a ese héroe en la lista.")


def eliminar_heroe(lista):
    """ Eliminar un personaje de la lista """
    nombre = input("\n¿Qué héroe quieres eliminar?: ")
    encontrado = False
    i = 0
    
    while i < len(lista) and not encontrado:
        h = lista[i]
        if h["nombre"].lower() == nombre.lower():
            respuesta = input("¿Seguro que quieres borrar a " + h['nombre'] + "? (s/n): ")
            
            if respuesta.lower() == 's':
                nombre_borrado = h['nombre']
                del lista[i]
                
                guardar_datos(lista)
                
                print("Héroe eliminado definitivamente.")
                # LOG INFO: Registro de eliminación (importante)
                logging.info(f"Eliminación: Héroe borrado -> {nombre_borrado}.")
            else:
                print("Operación cancelada.")
                logging.info(f"Eliminación cancelada por usuario para {h['nombre']}.")
            
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
        # F-strings para alinear columnas
        print(f"{'NOMBRE':<20} {'CLASE':<15} {'VIDA':<10}")
        print("-" * 45) 

        for h in lista:
            print(f"{h['nombre']:<20} {h['clase']:<15} {h['vida']:<10}")

    print("-" * 45)


def menu():
    """ Función principal """
    # LOG INFO: Inicio de sesión
    logging.info("--- INICIO DE APLICACIÓN ---")
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
            # LOG INFO: Fin de sesión
            logging.info("--- FIN DE APLICACIÓN ---")
            continuar = False
        else:
            print("Esa opción no existe, prueba otra vez.")

# Ejecutar el menú del programa
menu()