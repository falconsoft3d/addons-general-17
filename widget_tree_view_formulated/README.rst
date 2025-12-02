===========================
Tree View Formulated Widget
===========================

Widget personalizado para vistas tree de Odoo 17 que permite definir fórmulas en Python para calcular totales personalizados en las columnas.

Características
===============

* Define fórmulas personalizadas para cada columna
* Reemplaza automáticamente las sumas por defecto
* Soporta operaciones matemáticas complejas
* Compatible con campos numéricos, float y monetarios
* Evaluación dinámica de fórmulas con contexto de registros

Instalación
===========

1. Copiar el módulo en la carpeta de addons
2. Actualizar la lista de aplicaciones
3. Instalar el módulo "Tree View Formulated Widget"

Uso
===

Para usar este widget en una vista tree:

1. **Configurar la vista con el tipo personalizado:**

   .. code-block:: xml

      <record id="view_custom_tree" model="ir.ui.view">
          <field name="name">custom.tree.formulated</field>
          <field name="model">tu.modelo</field>
          <field name="arch" type="xml">
              <tree js_class="tree_formulated">
                  <!-- tus campos aquí -->
              </tree>
          </field>
      </record>

2. **Definir fórmulas en las columnas:**

   Usa el atributo ``options`` con la clave ``formulated`` para definir la fórmula:

   .. code-block:: xml

      <field name="fdo_m" options="{'formulated': 'fdo_orig + cte_orig'}"/>
      <field name="resultado" options="{'formulated': 'valor1 + valor2 - valor3'}"/>
      <field name="porcentaje" options="{'formulated': '(valor1 / valor2) * 100'}"/>

Ejemplos
========

**Ejemplo 1: Suma de dos columnas**

.. code-block:: xml

   <tree js_class="tree_formulated">
       <field name="fdo_orig" sum="Total FdO Original"/>
       <field name="cte_orig" sum="Total Cte Original"/>
       <field name="fdo_m" options="{'formulated': 'fdo_orig + cte_orig'}" sum="Total FdO-M"/>
   </tree>

En este ejemplo, la columna ``fdo_m`` mostrará la suma de ``fdo_orig + cte_orig`` en lugar del total por defecto.

**Ejemplo 2: Cálculos complejos**

.. code-block:: xml

   <tree js_class="tree_formulated">
       <field name="a" sum="Total A"/>
       <field name="m" sum="Total M"/>
       <field name="fdo_a" sum="Total FdO-A"/>
       <field name="cte_a" sum="Total Cte-A"/>
       <field name="fdo_m" sum="Total FdO-M"/>
       <field name="cte_m" sum="Total Cte-M"/>
       <field name="resultado" options="{'formulated': '(a + m + fdo_a + cte_a) - (fdo_m + cte_m)'}" sum="Total Resultado"/>
       <field name="porcentaje" options="{'formulated': '(resultado / a) * 100 if a != 0 else 0'}" sum="Porcentaje"/>
   </tree>

**Ejemplo 3: Operaciones matemáticas**

.. code-block:: xml

   <tree js_class="tree_formulated">
       <field name="precio" sum="Total Precio"/>
       <field name="cantidad" sum="Total Cantidad"/>
       <field name="descuento" sum="Total Descuento"/>
       <field name="total" options="{'formulated': '(precio * cantidad) - descuento'}" sum="Total"/>
       <field name="promedio" options="{'formulated': 'precio / cantidad > 0 ? precio / cantidad : 0'}" sum="Promedio"/>
   </tree>

**Ejemplo 4: Usando funciones de agregación (MAX, MIN, AVG)**

.. code-block:: xml

   <tree js_class="tree_formulated">
       <field name="producto"/>
       <field name="precio" sum="Total Precio"/>
       <field name="cantidad" sum="Total Cantidad"/>
       <field name="venta" sum="Total Venta"/>
       
       <!-- Mostrar el precio máximo de todos los registros -->
       <field name="precio_max" 
              options="{'formulated': 'MAX(\"precio\")'}" 
              string="Precio Máximo"/>
       
       <!-- Mostrar el precio mínimo de todos los registros -->
       <field name="precio_min" 
              options="{'formulated': 'MIN(\"precio\")'}" 
              string="Precio Mínimo"/>
       
       <!-- Mostrar el promedio de ventas -->
       <field name="venta_promedio" 
              options="{'formulated': 'AVG(\"venta\")'}" 
              string="Venta Promedio"/>
       
       <!-- Diferencia entre máximo y mínimo -->
       <field name="rango_precio" 
              options="{'formulated': 'MAX(\"precio\") - MIN(\"precio\")'}" 
              string="Rango de Precios"/>
       
       <!-- Promedio redondeado -->
       <field name="venta_promedio_redondeado" 
              options="{'formulated': 'Math.round(AVG(\"venta\"))'}" 
              string="Venta Promedio (redondeado)"/>
   </tree>

Sintaxis de Fórmulas
====================

Las fórmulas usan sintaxis JavaScript estándar:

* **Operadores aritméticos:** ``+``, ``-``, ``*``, ``/``, ``%``, ``**`` (potencia)
* **Operadores de comparación:** ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=``
* **Operador ternario:** ``condición ? valor_si_true : valor_si_false``
* **Funciones Math:** ``Math.abs()``, ``Math.round()``, ``Math.floor()``, ``Math.ceil()``, etc.

Funciones de Agregación Especiales
===================================

El widget incluye funciones especiales para calcular agregaciones sobre los valores individuales de cada registro (no sobre los totales):

* **MAX(campo)** - Devuelve el valor máximo de la columna entre todos los registros
* **MIN(campo)** - Devuelve el valor mínimo de la columna entre todos los registros
* **AVG(campo)** - Devuelve el promedio de la columna entre todos los registros
* **SUM(campo)** - Devuelve la suma de todos los valores de la columna
* **COUNT(campo)** - Devuelve el número de registros que tienen valor en ese campo

**Nota importante:** Cuando usas un nombre de campo directamente (ej: ``campo1 + campo2``), obtienes la SUMA de todos los valores. Para obtener otras agregaciones, usa las funciones especiales.

**Ejemplos de fórmulas:**

* ``fdo_orig + cte_orig`` - Suma simple (suma de totales)
* ``valor1 - valor2 + valor3`` - Operaciones múltiples
* ``(precio * cantidad) - descuento`` - Con paréntesis para precedencia
* ``valor1 / valor2 * 100`` - División y multiplicación
* ``valor > 0 ? valor * 1.21 : 0`` - Condicional (agregar IVA solo si es positivo)
* ``Math.round((valor1 + valor2) / 2)`` - Promedio redondeado
* ``Math.max(valor1, valor2, valor3)`` - Valor máximo entre totales

**Ejemplos con funciones de agregación:**

* ``MAX('precio')`` - El precio más alto de todos los registros
* ``MIN('cantidad')`` - La cantidad más baja de todos los registros
* ``AVG('total')`` - El promedio de todos los totales
* ``MAX('precio') - MIN('precio')`` - Diferencia entre el precio máximo y mínimo
* ``AVG('precio') * COUNT('precio')`` - Promedio multiplicado por cantidad de registros
* ``SUM('precio') / COUNT('precio')`` - Otra forma de calcular el promedio
* ``MAX('venta') > 1000 ? 'Alto' : 'Bajo'`` - Condicional basado en el valor máximo

Caso de uso real basado en tu imagen
=====================================

Para la vista que mostraste, podrías usar:

.. code-block:: xml

   <tree js_class="tree_formulated">
       <field name="estado"/>
       <field name="jefe"/>
       <field name="proyecto"/>
       <field name="custodio"/>
       <field name="a" sum="Total A"/>
       <field name="m" sum="Total M"/>
       <field name="fdo_orig" sum="Total FdO Orig"/>
       <field name="cte_orig" sum="Total Cte Orig"/>
       <field name="fdo_a" sum="Total FdO-A"/>
       <field name="cte_a" sum="Total Cte-A"/>
       <field name="fdo_m" options="{'formulated': 'fdo_orig + m'}" sum="Total FdO-M"/>
       <field name="cte_m" options="{'formulated': 'cte_orig + a'}" sum="Total Cte-M"/>
       <field name="a_p_m" sum="Total A/P-M"/>
       <field name="r_orig" sum="Total R-Orig"/>
       <field name="r_a" options="{'formulated': 'r_orig - fdo_a - cte_a'}" sum="Total R-A"/>
       <field name="pct_mbrut" sum="Avg %MBrut"/>
       <field name="pct_mbrut_a" sum="Avg %MBrut-A"/>
       <field name="pct_mnet" sum="Avg %MNet"/>
       <field name="pct_mnet_a" sum="Avg %MNet-A"/>
   </tree>

Notas Importantes
=================

* Los nombres de las variables en las fórmulas deben coincidir exactamente con los nombres de los campos
* Las fórmulas se evalúan sobre los totales de cada columna (suma de todos los valores)
* Si un campo no es numérico, se trata como 0 en la fórmula
* Los errores en las fórmulas se muestran como "Error" en el total
* Las fórmulas soportan JavaScript, no Python (a pesar del nombre del módulo)

Compatibilidad
==============

* Odoo 17.0

Créditos
========

**Autor:**

* Marlon Falcón Hernández

**Mantenedor:**

Este módulo es mantenido por Marlon Falcón Hernández.

https://www.marlonfalcon.com
