# Instalación de httpx para integración con TicketProo

## Requisitos

El módulo requiere la librería `httpx` para realizar las llamadas a la API de TicketProo.

## Instalación

### Opción 1: Con pip (recomendado)

```bash
pip3 install httpx
```

### Opción 2: Con el entorno virtual de Odoo

```bash
# Activar el entorno virtual de Odoo (si usas uno)
source /path/to/odoo-venv/bin/activate

# Instalar httpx
pip install httpx
```

### Opción 3: En el sistema

```bash
# Para Python 3
python3 -m pip install httpx

# O con sudo si es necesario
sudo pip3 install httpx
```

## Verificar instalación

Puedes verificar que httpx está instalado correctamente:

```bash
python3 -c "import httpx; print(httpx.__version__)"
```

Si no muestra errores y muestra la versión, está instalado correctamente.

## Configuración del Token

Después de instalar httpx y actualizar el módulo:

1. Ir a: **Ajustes → Ajustes Generales**
2. Buscar la sección: **TicketProo Integration**
3. Configurar:
   - **URL de API**: `https://ticketproo.com/api/landing-pages/1/submit/` (ya viene por defecto)
   - **Token de API**: `ce35e472-0579-4da4-ab1b-e051868c5ab6` (tu token)
4. Hacer clic en **Guardar**

## Notas

- Si httpx no está instalado, el módulo seguirá funcionando pero no enviará datos a TicketProo
- Los errores de la API no afectarán el registro de usuarios
- Todos los errores se registran en los logs de Odoo
