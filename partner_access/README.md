Products & Partners access MFH
=================================

Basado en los permisos de los usuarios, evita que se puedan crear productos,
clientes, proveedores, cuentas contables o cuentas analíticas en las vistas:

* Orden de compra
* Orden de venta
* Presupuesto de compra
* Presupuesto de venta
* Facturas de proveedor
* Facturas de clientes
* Guía de despacho / Albaranes
* Productos
* Clientes
* Proveedores
* Cuentas Contables
* Cuentas Analíticas

Configuración
-------------

Por defecto, cualquier usuario con los permisos necesarios podrá crear y editar
los productos, clientes, proveedores, cuentas contables y cuentas analíticas, si
se desea restringir el acceso se debe ir hasta ``Configuración`` > ``Usuarios`` >
``Usuarios`` y seleccionamos al usuario que se le quiere restringir los permisos,
marcamos la opción según el caso:

* Crear/Editar Clientes y Proveedores
* Crear/Editar Productos
* Crear/Editar Cuentas Contables/Analíticas

Y ya con esto, las vistas no le permitirán acceder a la opción de creación o
edición del modelo seleccionado. Estos permisos solo se aplican a nivel de las
vistas, por lo que no afectará la edición de los modelos mientras maneje otros
modelos, por ejemplo, al hacer una venta, el stock del producto cambiará como
se debe, por lo que la edición del producto seguiría funcionando indirectamente.
