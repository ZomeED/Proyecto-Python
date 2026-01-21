# Proyecto - Python: The Tower

**Versión:** 0.2 (Segunda Entrega: Persistencia y Logs)  
**Autor:** José Antonio Zomeño Pardo  
**Lenguaje:** Python 3  

## 📖 Descripción del Proyecto
**The Tower** será un minijuego de rol (RPG) por consola. El objetivo final será gestionar un héroe que debe ascender por los diferentes pisos de una torre, combatiendo enemigos y obteniendo recompensas hasta derrotar al Boss Final.

## ⚙️ Funcionalidades Actuales
En esta versión se ha mejorado el **sistema de gestión** añadiendo persistencia de datos y auditoría de eventos.

### Gestión de Personajes (CRUD)
1.  **Crear Héroe:** - Validación de nombre único (evita duplicados).
    - Selección de Clase (Humano, Tanque, Duende) con estadísticas automáticas.
2.  **Buscar Héroe:** Muestra la ficha completa (Vida, Ataque, Velocidad).
3.  **Modificar:** Permite cambiar el nombre de un personaje existente.
4.  **Eliminar:** Borrado de personajes con confirmación de seguridad (`s/n`).
5.  **Mostrar datos:** Tabla visual mejorada (alineación perfecta con `f-strings`) con todos los personajes activos.

### Nuevas Implementaciones Técnicas
6.  **Persistencia de Datos (JSON):** - La información ya no se pierde al cerrar el programa.
    - Los héroes se guardan automáticamente en el fichero `datos_heroes.json`.
    - Uso de las librerías `json` (`dumps` y `loads`) con control de errores.

7.  **Sistema de Logging (Registro):**
    - Se registran los eventos importantes de la ejecución en el fichero `registro_partida.log`.
    - Diferenciación de niveles de gravedad:
        - **INFO:** Operaciones normales (crear, guardar, cargar).
        - **WARNING:** Errores de usuario no críticos (nombres vacíos, opciones incorrectas).
        - **ERROR:** Fallos técnicos con traza completa (`traceback`).

## 📂 Archivos del Proyecto
* `main.py`: Código fuente principal.
* `datos_heroes.json`: Base de datos de los personajes.
* `registro_partida.log`: Fichero de historial de eventos.

## 🔜 Hoja de Ruta (Próximamente)
* [ ] Sistema de combate por turnos (Héroe vs Enemigo).
* [ ] Bucle de juego principal (Subir de piso).
* [ ] Sistema de recompensas (Pociones y mejoras).
* [ ] Jefe Final (Boss).
