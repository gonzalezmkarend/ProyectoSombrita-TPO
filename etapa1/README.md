# etapa1/

Código de la Entrega 1, sin cambios. Queda como referencia: el programa actual no lo usa.

| Archivo | Qué es |
|---|---|
| `tpo_etapa1_carpas.py` | Programa completo de la Etapa 1, en un solo archivo y con listas de listas. |
| `boceto_menu.py` | Esqueleto del menú: cada opción describe lo que iba a hacer. |

Para correr la Etapa 1, desde esta carpeta:

```bash
python tpo_etapa1_carpas.py
```

## Qué cambió en la Etapa 2

- Un archivo por menú en lugar de un solo archivo.
- Diccionarios en lugar de listas de listas. La tabla completa está en el [README principal](../README.md#contrato-de-datos).
- `datetime` en lugar de la validación manual de fechas.
- Quicksort recursivo en lugar de ordenamiento por inserción.
- `tabulate` y `colorama` para la pantalla.
- Datos guardados en JSON, que antes se perdían al cerrar.
- Pruebas automáticas con pytest.
- El menú de clientes ya no existe: los clientes se registran al cargar una reserva, y se buscan desde "Buscar reservas por cliente".
