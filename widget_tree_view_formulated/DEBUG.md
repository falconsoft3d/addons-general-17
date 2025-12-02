# Debug del Widget Tree Formulated

## Para verificar que el widget está funcionando:

1. Abre la consola del navegador (F12 → Console)
2. En tu vista tree, ejecuta:

```javascript
// Ver si el widget está registrado
console.log(odoo.__DEBUG__.services['view_registry'].get('tree_formulated'));

// Ver los totales calculados (cuando estés en la vista)
// Busca en la consola mensajes del widget
```

## Problemas comunes:

### 1. El módulo no está actualizado
- Ve a Apps → Tree View Formulated Widget → Actualizar

### 2. La fórmula usa el nombre incorrecto del campo
- Verifica que el nombre en la fórmula coincida EXACTAMENTE con el nombre del campo
- Ejemplo: si el campo es `cte_mes`, la fórmula debe usar `cte_mes` (no `cte_month` ni `cteMes`)

### 3. El campo no tiene valores numéricos
- El widget solo suma valores numéricos
- Si un campo es texto o está vacío, se trata como 0

### 4. La fórmula tiene un error de sintaxis
- Verifica que uses sintaxis JavaScript correcta
- Correcto: `cte_mes * 2`
- Incorrecto: `cte_mes x 2`

## Ejemplo de debugging en la consola:

Cuando estés en la vista tree, ejecuta:

```javascript
// Ver todos los registros cargados
const records = document.querySelector('.o_list_renderer')?.__owl__?.component?.props?.list?.records;
console.log('Registros:', records);

// Ver valores de un campo específico
records?.forEach((r, i) => console.log(`Registro ${i}: cte_mes =`, r.data.cte_mes));

// Calcular manualmente la suma
const suma = records?.reduce((acc, r) => acc + (r.data.cte_mes || 0), 0);
console.log('Suma manual de cte_mes:', suma);
console.log('Resultado esperado (suma * 2):', suma * 2);
```

## Si ves "Error" en el total:

Revisa la consola del navegador, debería mostrar el error específico.
