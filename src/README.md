# src/

Código del programa. `main.py`, en la raíz, los integra. La descripción general está en el [README principal](../README.md).

Dentro de cada menú, las funciones de lógica reciben los datos por parámetro y devuelven un resultado, sin usar `input()` ni `print()`. Las funciones `_menu_*`, `_opcion_*`, `_leer_*` y `_mostrar_*` son las que hablan con el usuario.

Los imports usan `from src.comunes import ...`, porque el programa siempre arranca desde `main.py`, en la raíz.

## comunes.py

Constantes y funciones que usan todos los módulos: fechas, ordenamiento, consultas compartidas, pantalla y teclado. No importa ningún otro módulo del proyecto.

| Función | Qué hace |
|---|---|
| `_validar_fecha` | Verifica que una cadena tenga formato "dd/mm/aaaa" y represente una fecha existente. |
| `_texto_a_fecha` | Convierte una fecha "dd/mm/aaaa" en un objeto datetime para poder compararla. |
| `_se_superponen` | Indica si dos rangos de fechas comparten al menos un día. |
| `_quicksort` | Ordena una lista de menor a mayor con quicksort recursivo, según una función clave. |
| `_consultar_estado_carpa` | Obtiene el estado de una carpa en un rango de fechas. |
| `_esta_ocupada` | Indica si una carpa tiene alguna reserva superpuesta a un rango de fechas. |
| `_nombre_cliente` | Obtiene el nombre de un cliente a partir de su DNI. |
| `_mostrar_error` | Muestra un mensaje de error en color rojo. |
| `_mostrar_exito` | Muestra un mensaje de éxito en color verde. |
| `_mostrar_resultado` | Muestra un mensaje según el resultado de una operación. |
| `_mostrar_menu` | Muestra un menú como tabla, con el título resaltado en color. |
| `_mostrar_tabla` | Muestra datos en una tabla, o un aviso si no hay datos. |
| `_leer_entero` | Solicita un número entero por teclado hasta que sea válido. |
| `_leer_texto` | Solicita un texto no vacío por teclado. |
| `_leer_fecha` | Solicita una fecha "dd/mm/aaaa" por teclado hasta que sea válida. |
| `_leer_rango_fechas` | Solicita dos fechas, desde y hasta, hasta que formen un rango válido. |

## persistencia.py

Lectura y escritura de `datos/sombrita.json`, con el manejo de archivos inexistentes o dañados. Importa solo `comunes`.

| Función | Qué hace |
|---|---|
| `_cargar_datos_iniciales` | Genera datos de ejemplo para usar cuando no hay un archivo de datos utilizable. |
| `_guardar_datos` | Guarda todas las estructuras en un único archivo JSON. |
| `_convertir_datos` | Valida lo leído del JSON y lo convierte a las estructuras del contrato de datos. |
| `_apartar_archivo_danado` | Renombra un archivo dañado para que el próximo guardado no lo pise. |
| `_cargar_datos` | Carga las estructuras desde el archivo JSON. |

## menu_carpas.py

Lógica y submenú de carpas. Importa `comunes` y `persistencia`.

| Función | Qué hace |
|---|---|
| `_registrar_carpa` | Da de alta una carpa nueva, activa por defecto. |
| `_modificar_carpa` | Cambia el número de una carpa y actualiza sus reservas. |
| `_cambiar_estado_carpa` | Activa o inactiva una carpa (borrado lógico). |
| `_listar_carpas` | Obtiene las carpas ordenadas por número. |
| `_mostrar_carpas` | Muestra carpas en una tabla. |
| `_menu_carpas` | Ejecuta el submenú de gestión de carpas. |

## menu_reservas.py

Lógica y submenú de clientes, reservas y alquileres. Importa `comunes` y `persistencia`.

| Función | Qué hace |
|---|---|
| `_normalizar_nombre` | Elimina espacios sobrantes y capitaliza cada palabra de un nombre. |
| `_validar_telefono` | Verifica que un teléfono contenga solo dígitos, espacios, "+" o "-". |
| `_registrar_cliente` | Da de alta un cliente con el nombre normalizado. |
| `_buscar_cliente_por_nombre` | Busca clientes cuyo nombre contenga un texto, sin distinguir mayúsculas. |
| `_buscar_reserva` | Busca una reserva por carpa, cliente y fecha de inicio. |
| `_registrar_reserva` | Da de alta una reserva o alquiler de una carpa para un cliente. |
| `_cancelar_reserva` | Da de baja una reserva. |
| `_cambiar_estado_reserva` | Cambia el estado de una reserva a "reservada" o "alquilada". |
| `_ordenar_reservas` | Ordena las reservas por fecha de inicio o por número de carpa. |
| `_consultar_reservas_cliente` | Obtiene las reservas de un cliente ordenadas por fecha de inicio. |
| `_buscar_reservas_por_texto` | Busca reservas por DNI o por parte del nombre del cliente. |
| `_reservas_del_dia` | Obtiene las reservas vigentes en una fecha, ordenadas por número de carpa. |
| `_leer_estado_reserva` | Solicita por teclado el estado de una reserva hasta que sea válido. |
| `_mostrar_reservas` | Muestra reservas en una tabla, con el nombre de cada cliente. |
| `_opcion_registrar_reserva` | Pide por teclado los datos de una reserva y la registra. Si el DNI no existe, también pide los datos del cliente y lo registra. |
| `_menu_reservas` | Ejecuta el submenú de gestión de reservas y alquileres. |

## menu_estadisticas.py

Lógica y submenú de estadísticas. Solo lee los datos, así que importa únicamente `comunes`.

| Función | Qué hace |
|---|---|
| `_carpas_ocupadas` | Obtiene los números de carpa con alguna reserva superpuesta a un rango de fechas. |
| `_carpas_libres` | Obtiene las carpas activas sin ninguna reserva en un rango de fechas. |
| `_calcular_ocupacion` | Calcula el porcentaje de carpas activas con alguna reserva en un rango de fechas. |
| `_dnis_con_reservas` | Obtiene los DNI distintos que aparecen en las reservas. |
| `_contar_reservas_cliente` | Cuenta las reservas de un cliente. |
| `_cliente_con_mas_reservas` | Encuentra el cliente con mayor cantidad de reservas. |
| `_menu_estadisticas` | Ejecuta el submenú de estadísticas. |
