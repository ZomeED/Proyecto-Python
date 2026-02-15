import json
import logging

"""
Proyecto: The Tower - Minijuego de rol
Gestión de personajes usando Clases (POO) y Herencia con persistencia en JSON y sistema de Logging.
"""

ARCHIVO_JSON = "datos_heroes.json"
ARCHIVO_LOG = "registro_partida.log"


# --- CLASES ---

class Heroe:
    """
    Clase Base.
    Datos que tiene cualquier personaje por defecto.
    """

    def __init__(self, nombre, clase, vida, ataque, velocidad):
        self.nombre = nombre
        self.clase = clase
        self.vida = vida
        self.ataque = ataque
        self.velocidad = velocidad

    def a_diccionario(self):
        """ Convertir el objeto en diccionario para poder guardarlo en JSON """
        # __dict__ para que Python devuelva los datos del objeto como un diccionario
        return self.__dict__


class Enemigo(Heroe):
    """
    Subclase para los enemigos.
    Hereda Héroe y añade 'recompensa'.
    """

    def __init__(self, nombre, clase, vida, ataque, velocidad, recompensa):

        super().__init__(nombre, clase, vida, ataque, velocidad)
        self.recompensa = recompensa


# --- CONFIGURACIÓN DEL SISTEMA DE REGISTRO (Logging) ---

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
    Lee el fichero JSON y convierte los diccionarios en OBJETOS.
    """
    try:
        fichero = open(ARCHIVO_JSON, "r")
        datos_recuperados = json.load(fichero)
        fichero.close()

        lista_objetos = []

        for d in datos_recuperados:
            # Si el diccionario tiene 'recompensa', es que era un Enemigo
            if "recompensa" in d:
                nuevo = Enemigo(d['nombre'], d['clase'], d['vida'], d['ataque'], d['velocidad'], d['recompensa'])
            else:
                nuevo = Heroe(d['nombre'], d['clase'], d['vida'], d['ataque'], d['velocidad'])
            lista_objetos.append(nuevo)

        # Mensaje INFO (nivel 20): Se registrará en el fichero, pero no en la consola.
        logging.info("Sistema: Datos cargados y convertidos a objetos correctamente.")
        return lista_objetos

    except Exception as e:
        # Mensaje WARNING (nivel 30): Se registra en fichero
        logging.warning(f"Sistema: No se encontró fichero previo o está vacío. Se inicia lista nueva. Detalle: {e}")
        return []


def guardar_datos(lista):
    """
    Guarda los datos en JSON y los objetos se convierten a diccionarios.
    """
    try:
        lista_para_guardar = [h.a_diccionario() for h in lista]

        texto_json = json.dumps(lista_para_guardar, indent=4)
        fichero = open(ARCHIVO_JSON, "w")
        fichero.write(texto_json)
        fichero.close()

        logging.info("Sistema: Datos guardados exitosamente en fichero JSON.")

    except Exception as e:
        print(f"Error crítico al guardar: {e}")
        logging.error(f"Error CRÍTICO guardando datos: {e}", exc_info=True)


# --- FUNCIONES DE GESTIÓN ---

def insertar_heroe(lista):
    """ Función para instanciar clases según la elección del usuario """
    print("\n--- REGISTRO DE ENTRADA ---")

    # Preguntar si es Héroe o Enemigo
    print("1. Héroe (Normal)")
    print("2. Enemigo (Especial)")
    tipo_registro = input("Selecciona tipo: ")

    nombre = input("Introduce el nombre: ")
    es_valido = True

    if len(nombre) == 0:
        print("Error: El nombre no puede estar en blanco.")
        logging.warning("Creación fallida: Nombre vacío.")
        es_valido = False

    # Comprobar nombre por si ya existe
    if es_valido:
        for h in lista:
            if h.nombre == nombre:
                print("Error: Ya existe ese nombre.")
                logging.warning(f"Creación fallida: El nombre '{nombre}' ya existe.")
                es_valido = False

    if es_valido:
        print("\n Clases disponibles: 1. Humano | 2. Tanque | 3. Duende")
        try:
            opcion = int(input("Elige una clase (1-3): "))

            # Stats
            stats = {1: ("Humano", 60, 15, 20), 2: ("Tanque", 70, 20, 10), 3: ("Duende", 50, 15, 30)}

            if opcion in stats:
                clase, vida, ataque, velocidad = stats[opcion]

                # Asignar experiencia si es un enemigo
                if tipo_registro == "2":
                    xp = int(input("¿Cuánta experiencia da al ser derrotado?: "))
                    nuevo_personaje = Enemigo(nombre, clase, vida, ataque, velocidad, xp)
                else:
                    nuevo_personaje = Heroe(nombre, clase, vida, ataque, velocidad)

                # Guardar objeto en la lista
                lista.append(nuevo_personaje)
                guardar_datos(lista)

                print(f"--> ¡Registrado! {nombre} ha entrado en la torre.")
                logging.info(f"Acción: Creado {type(nuevo_personaje).__name__} -> {nombre}")

            else:
                print("Opción incorrecta.")
        except ValueError:
            print("Error: Debes introducir un número entero.")
            logging.error("Error de usuario: Entrada no válida en creación.", exc_info=True)


def buscar_heroe(lista):
    """ Buscar un héroe por el nombre """
    nombre_buscado = input("\nIntroduce nombre para buscar: ")
    encontrado = False

    for h in lista:
        if h.nombre.lower() == nombre_buscado.lower():
            print("\n--- FICHA ENCONTRADA ---")
            print(f"Nombre: {h.nombre}")
            print(f"Tipo:   {type(h).__name__}")
            print(f"Vida:   {h.vida}")

            # Si el objeto es de tipo Enemigo, muestra su atributo de recompensa
            if isinstance(h, Enemigo):
                print(f"Botín:  {h.recompensa} XP")

            encontrado = True
            logging.info(f"Consulta: Se visualizaron datos de {h.nombre}.")
            break

    if not encontrado:
        print("No se ha encontrado a nadie.")


def modificar_heroe(lista):
    """ Cambiar nombre accediendo al atributo .nombre """
    busqueda = input("\n¿A quién quieres modificar?: ")
    encontrado = False

    for h in lista:
        if h.nombre.lower() == busqueda.lower():
            print(f"Modificando a: {h.nombre}")
            nuevo_nombre = input("Introduce el nuevo nombre: ")

            if len(nuevo_nombre) > 0:
                nombre_antiguo = h.nombre
                h.nombre = nuevo_nombre

                guardar_datos(lista)
                print("Nombre cambiado correctamente.")
                logging.info(f"Modificación: '{nombre_antiguo}' pasó a ser '{nuevo_nombre}'.")
            else:
                print("Error: Nombre vacío.")
            encontrado = True
            break

    if not encontrado:
        print("No se encuentra en la lista.")


def eliminar_heroe(lista):
    """ Elimina un objeto de la lista """
    nombre = input("\n¿A quién quieres eliminar?: ")
    for i, h in enumerate(lista):
        if h.nombre.lower() == nombre.lower():
            confirmar = input(f"¿Borrar a {h.nombre}? (s/n): ")
            if confirmar.lower() == 's':
                nombre_borrado = h.nombre
                lista.pop(i)  # Eliminar la instancia de la lista
                guardar_datos(lista)
                print("Eliminado.")
                logging.info(f"Eliminación: {nombre_borrado} borrado.")
            return
    print("No existe.")


def mostrar_todos(lista):
    """ Muestra el listado accediendo a los atributos de cada objeto """
    print("\n--- LISTA DE PERSONAJES (OBJETOS) ---")

    if not lista:
        print("La torre está vacía.")
    else:
        # Cabecera de la tabla
        print(f"{'NOMBRE':<15} {'TIPO':<10} {'VIDA':<8} {'XP':<10}")
        print("-" * 50)
        for h in lista:
            # Identificar el tipo para mostrar diferente info
            tipo = "Enemigo" if isinstance(h, Enemigo) else "Héroe"
            # Solo los enemigos tienen el atributo .recompensa
            extra = f"{h.recompensa} XP" if isinstance(h, Enemigo) else "---"
            print(f"{h.nombre:<15} {tipo:<10} {h.vida:<8} {extra:<10}")
    print("-" * 50)


def menu():
    """ Función principal """
    logging.info("--- INICIO DE SESIÓN ---")

    while True:
        print("\n=== THE TOWER - GESTIÓN POO ===")
        print("1. Crear (Héroe/Enemigo)")
        print("2. Buscar")
        print("3. Modificar")
        print("4. Eliminar")
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
            print("Cerrando sistema...")
            logging.info("--- FIN DE SESIÓN ---")
            break
        else:
            print("Opción no válida.")


# --- INICIO DEL PROGRAMA ---
lista_heroes = cargar_datos()
menu()
