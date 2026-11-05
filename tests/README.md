# tests/

Pruebas automáticas con pytest. Se corren desde la raíz del repo:

```bash
python -m pytest
python -m pytest -v
python -m pytest tests/test_comunes.py
```

## Recursos compartidos

`conftest.py` define las fixtures que usan las pruebas:

| Fixture | Contenido |
|---|---|
| `carpas`, `clientes`, `reservas` | Datos de prueba nuevos para cada prueba. |
| `simular_teclado` | Reemplaza `input()` por una lista de respuestas. |

Las pruebas de persistencia e integración usan `tmp_path`, por lo que no modifican `datos/sombrita.json`.

## Cobertura

Casos normales, límite, datos inválidos, colecciones vacías, búsquedas con y sin resultado, reglas de negocio, persistencia y errores de archivo.

## Qué prueba cada archivo

### test_comunes.py

Fechas, quicksort, consultas compartidas y lectura por teclado (`src/comunes.py`).

| Prueba | Qué comprueba |
|---|---|
| `test_validar_fecha_valida` | Caso normal. |
| `test_fecha_de_hoy_es_valida` | Postcondición: el texto respeta el formato que usa el resto del programa. |
| `test_validar_fecha_dia_inexistente` | Abril tiene 30 días. |
| `test_validar_fecha_29_febrero_bisiesto` | Límite: 2028 es bisiesto. |
| `test_validar_fecha_29_febrero_no_bisiesto` | Límite: 2027 no es bisiesto. |
| `test_validar_fecha_formatos_invalidos` | Dato inválido: no respeta dd/mm/aaaa. No debe lanzar una excepción. |
| `test_se_superponen_rangos_separados` | Rangos sin días en común. |
| `test_se_superponen_comparten_un_dia` | Límite: comparten solo el último día de uno y el primero del otro. |
| `test_se_superponen_uno_dentro_del_otro` | Un rango contiene por completo al otro. |
| `test_se_superponen_compara_fechas_y_no_texto` | Como texto "15/01" es mayor que "01/02", pero como fecha es anterior. |
| `test_quicksort_lista_vacia` | Colección vacía: caso base de la recursión. |
| `test_quicksort_ordena_con_repetidos` | Caso normal con elementos repetidos. |
| `test_quicksort_usa_la_clave` | Ordena según la función clave, no por el elemento completo. |
| `test_quicksort_no_modifica_la_original` | Postcondición: devuelve una lista nueva. |
| `test_quicksort_conserva_orden_de_claves_iguales` | Postcondición: los elementos con la misma clave no se reordenan. |
| `test_quicksort_lista_grande_ya_ordenada` | Límite: el pivote central evita superar el límite de recursión de Python. |
| `test_consultar_estado_alquilada` | El rango cae sobre una reserva alquilada. |
| `test_consultar_estado_reservada` | El rango cae sobre una reserva sin pagar. |
| `test_consultar_estado_libre_sin_superposicion` | La carpa tiene reservas, pero en otras fechas. |
| `test_consultar_estado_otra_carpa` | Una reserva de la carpa 1 no ocupa a la carpa 2. |
| `test_esta_ocupada` | Ocupada en el rango de una reserva y libre fuera de él. |
| `test_nombre_cliente` | Búsqueda exitosa y búsqueda sin resultado. |
| `test_leer_entero_reintenta` | Rechaza texto y valores menores al mínimo hasta recibir uno válido. |
| `test_leer_texto_reintenta_y_limpia` | Rechaza texto vacío y quita los espacios sobrantes. |
| `test_leer_fecha_reintenta` | Rechaza una fecha inexistente. |
| `test_leer_rango_rechaza_invertido` | Vuelve a pedir ambas fechas si desde es posterior a hasta, y devuelve una tupla. |

### test_menu_carpas.py

Lógica de carpas (`src/menu_carpas.py`).

| Prueba | Qué comprueba |
|---|---|
| `test_registrar_carpa_nueva` | Caso normal: queda registrada y activa. |
| `test_registrar_carpa_numero_no_positivo` | Dato inválido: 0 y negativos no se registran. |
| `test_registrar_carpa_repetida` | Regla del negocio: el número es único. Tampoco cambia el estado de la existente. |
| `test_modificar_carpa_actualiza_sus_reservas` | Regla del negocio: las reservas siguen apuntando a la carpa renombrada. |
| `test_modificar_carpa_conserva_estado` | Una carpa inactiva sigue inactiva con el número nuevo. |
| `test_modificar_carpa_inexistente` | Búsqueda sin resultado. |
| `test_modificar_carpa_numero_en_uso` | Regla del negocio: el número nuevo no puede estar en uso. No modifica nada. |
| `test_modificar_carpa_numero_invalido` | Dato inválido: el número nuevo debe ser mayor a 0. |
| `test_inactivar_carpa_sin_reservas` | Borrado lógico: la carpa sigue existiendo, inactiva. |
| `test_inactivar_carpa_con_reservas` | Regla del negocio: no se puede inactivar una carpa con reservas. |
| `test_activar_carpa` | Una carpa inactiva vuelve a estar activa. |
| `test_cambiar_estado_carpa_inexistente` | Búsqueda sin resultado: no crea la carpa. |
| `test_listar_carpas_ordenadas` | Ordena por número aunque se hayan cargado desordenadas. |
| `test_listar_carpas_solo_activas` | Excluye las inactivas. |
| `test_listar_carpas_vacio` | Colección vacía. |

### test_menu_reservas.py

Lógica de clientes y reservas (`src/menu_reservas.py`).

| Prueba | Qué comprueba |
|---|---|
| `test_normalizar_nombre` | Quita espacios sobrantes y capitaliza, incluso con tildes. |
| `test_validar_telefono_valido` | Formatos aceptados; 6 dígitos es el mínimo. |
| `test_validar_telefono_invalido` | Dato inválido: letras, menos de 6 dígitos o vacío. |
| `test_registrar_cliente_normaliza` | Caso normal: guarda el nombre normalizado. |
| `test_registrar_cliente_dni_repetido` | Regla del negocio: el DNI es único y no se pisan los datos existentes. |
| `test_registrar_cliente_datos_invalidos` | Dato inválido: DNI, nombre o teléfono. No agrega nada. |
| `test_buscar_cliente_por_nombre_sin_mayusculas` | Búsqueda exitosa por parte del nombre, sin distinguir mayúsculas. |
| `test_buscar_cliente_por_nombre_sin_resultado` | Búsqueda sin resultado. |
| `test_registrar_reserva_valida` | Caso normal. |
| `test_registrar_reserva_de_un_dia` | Límite: desde y hasta pueden ser el mismo día. |
| `test_registrar_reserva_estado_por_defecto` | Sin indicar estado, queda como reservada. |
| `test_registrar_reserva_rechazada` | Regla del negocio o dato inválido: devuelve False y no agrega nada. |
| `test_registrar_reserva_contigua` | Límite: puede empezar el día siguiente a que termina otra reserva. |
| `test_registrar_reserva_misma_fecha_otra_carpa` | La superposición solo importa dentro de la misma carpa. |
| `test_buscar_reserva` | Búsqueda exitosa (devuelve el índice) y sin resultado (-1). |
| `test_cancelar_reserva` | Elimina solamente la reserva indicada. |
| `test_cancelar_primera_reserva` | Elimina la reserva buscada aunque no sea la última de la lista. |
| `test_cancelar_reserva_inexistente` | Búsqueda sin resultado: no elimina nada. |
| `test_cambiar_estado_a_alquilada` | Caso normal: se pagó la reserva. |
| `test_cambiar_estado_inexistente_o_invalido` | Reserva inexistente o estado inválido: no modifica nada. |
| `test_ordenar_por_fecha_real` | Enero va antes que febrero, aunque como texto "01/02" sea menor que "15/01". |
| `test_ordenar_por_carpa_sin_modificar_original` | Ordena por carpa y conserva la lista original. |
| `test_ordenar_lista_vacia` | Colección vacía. |
| `test_consultar_reservas_cliente` | Filtra por DNI; un DNI sin reservas devuelve una lista vacía. |
| `test_buscar_reservas_por_dni` | Un texto de solo dígitos se busca como DNI. |
| `test_buscar_reservas_por_nombre` | Cualquier otro texto se busca en el nombre, sin distinguir mayúsculas. |
| `test_buscar_reservas_sin_resultado` | Búsqueda sin resultado por nombre y por DNI. |
| `test_reservas_del_dia` | Límite: los extremos del rango cuentan como vigentes. |
| `test_leer_fecha_del_dia_hoy` | La opción Hoy devuelve la fecha actual sin pedir que se escriba. |
| `test_leer_fecha_del_dia_otra_fecha` | La opción Otra fecha pide la fecha y rechaza una inexistente. |
| `test_leer_fecha_del_dia_opcion_invalida` | Una opción inexistente avisa y vuelve a preguntar. |

### test_menu_estadisticas.py

Lógica de estadísticas (`src/menu_estadisticas.py`).

| Prueba | Qué comprueba |
|---|---|
| `test_carpas_ocupadas_devuelve_conjunto` | Dos reservas de la misma carpa cuentan como una sola carpa ocupada. |
| `test_carpas_ocupadas_sin_coincidencias` | Ninguna reserva cae en el rango. |
| `test_carpas_libres_excluye_ocupadas_e_inactivas` | La 1 está ocupada y la 3 está inactiva: solo queda la 2. |
| `test_carpas_libres_ordenadas` | Devuelve los números de menor a mayor. |
| `test_carpas_libres_sin_carpas` | Colección vacía. |
| `test_ocupacion_parcial` | Una de las dos carpas activas está ocupada: 50 %. |
| `test_ocupacion_sin_reservas_en_rango` | Ninguna carpa ocupada: 0 %. |
| `test_ocupacion_total` | Todas las carpas activas ocupadas: 100 %. |
| `test_ocupacion_sin_carpas_activas` | Colección vacía: no debe dividir por cero. |
| `test_ocupacion_ignora_carpas_inactivas` | Una reserva sobre una carpa inactiva no cuenta para el porcentaje. |
| `test_dnis_con_reservas` | Devuelve DNI distintos, sin repetir. |
| `test_contar_reservas_cliente` | Cuenta por DNI; un DNI sin reservas tiene 0. |
| `test_cliente_con_mas_reservas` | Caso normal: Juan tiene dos reservas y María una. |
| `test_cliente_con_mas_reservas_empate` | Límite: con una reserva cada uno, gana el DNI menor. |
| `test_cliente_con_mas_reservas_sin_reservas` | Colección vacía. |

### test_persistencia.py

Guardado, carga y archivos dañados (`src/persistencia.py`).

| Prueba | Qué comprueba |
|---|---|
| `test_guardar_y_cargar_devuelve_lo_mismo` | Persistencia: lo cargado es igual a lo guardado, con las claves como int. |
| `test_cargar_convierte_claves_a_int` | JSON guarda las claves como texto: al cargar tienen que volver a ser int. |
| `test_guardar_conserva_tildes` | ensure_ascii=False: el archivo es legible, con "Pérez" y no con "P\u00e9rez". |
| `test_guardar_crea_la_carpeta` | Si la carpeta no existe, se crea. |
| `test_guardar_sin_poder_escribir_no_falla` | Error de archivo: la ruta es una carpeta. Avisa y el programa sigue. |
| `test_cargar_archivo_inexistente` | Error de archivo: usa los datos iniciales y crea el archivo. |
| `test_cargar_json_corrupto_conserva_el_archivo` | Error de archivo: no se cae, avisa y conserva una copia con el contenido original. |
| `test_cargar_corrupto_no_pisa_respaldos_anteriores` | Dos archivos dañados seguidos generan dos copias distintas. |
| `test_guardar_despues_de_corrupto_no_pisa_la_copia` | El guardado que sigue al arranque no destruye el archivo dañado. |
| `test_cargar_contenido_invalido` | JSON bien formado con datos inválidos: se trata como archivo dañado. |
| `test_datos_iniciales_respetan_las_reglas` | Los datos de ejemplo cumplen las reglas que el programa exige a cualquier reserva. |

### test_integracion.py

El programa completo, de `main()` al archivo, simulando lo que escribe el usuario.

| Prueba | Qué comprueba |
|---|---|
| `test_salir_directo` | Abrir y salir: crea el archivo con los datos de ejemplo. |
| `test_opciones_invalidas_no_rompen` | Opciones inexistentes y texto en cada menú: avisa y sigue. |
| `test_registrar_carpa_persiste_sin_salir` | Guarda después de cada cambio: si se corta antes de salir, el dato ya está en disco. |
| `test_datos_siguen_al_reabrir` | Cerrar y volver a abrir: los datos siguen ahí. |
| `test_reserva_con_cliente_nuevo` | DNI desconocido: pide los datos del cliente, y registra cliente y reserva. |
| `test_reserva_con_cliente_existente_no_pide_datos` | DNI conocido: pasa directo a las fechas. |
| `test_reserva_telefono_invalido_no_registra_nada` | Teléfono inválido: avisa y no pide fechas ni agrega datos. |
| `test_cliente_nuevo_se_guarda_aunque_falle_la_reserva` | El cliente ya quedó registrado: se guarda en el momento, aunque la carpa no exista. |
| `test_reserva_carpa_ocupada_rechazada` | La carpa 1 ya está alquilada del 01/01 al 15/01/2027 en los datos de ejemplo. |
| `test_cancelar_y_cambiar_estado` | Cambia el estado de una reserva, cancela otra y lo guarda. |
| `test_listados_de_reservas` | Cada opción de listado muestra los resultados, y avisa si no hay. |
| `test_menu_carpas_completo` | Recorre las opciones de carpas: listar, modificar, inactivar, activar y consultar. |
| `test_menu_estadisticas_completo` | Datos de ejemplo: 9 carpas activas y 2 ocupadas (la 2 y la 3) del 16 al 31/01/2027. |
| `test_ctrl_c_guarda_y_sale` | Ctrl+C durante el menú: no muestra un error de Python, guarda y sale prolijo. |
| `test_archivo_danado_no_impide_arrancar` | Con el archivo roto, el programa arranca, guarda y conserva la copia dañada. |
