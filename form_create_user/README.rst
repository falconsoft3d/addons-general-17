==================================
Formulario de Auto-Creación de Usuarios
==================================

Módulo para Odoo 17 que permite a usuarios públicos auto-registrarse y crear automáticamente usuarios internos.

Características
===============

* **Formulario web público** para registro de usuarios
* **Clonación automática** de permisos desde un usuario plantilla
* **Generación automática** de contraseñas seguras
* **Creación de oportunidades** en CRM con los datos del formulario
* **Visualización de credenciales** generadas al usuario
* **Integración con TicketProo API** para envío automático de registros

Instalación
===========

1. Copiar el módulo en la carpeta de addons de Odoo
2. Instalar la librería httpx: ``pip3 install httpx``
3. Actualizar la lista de aplicaciones
4. Instalar el módulo "Form Create User MFH"

Configuración
=============

1. **Configurar Usuario Plantilla:**
   
   * Ir a Ajustes → Usuarios y Empresas → Usuarios
   * Seleccionar el usuario que desea usar como plantilla
   * Activar el campo "Usuario Plantilla"
   * Este usuario debe tener configurados todos los permisos y grupos que se quieren copiar a los nuevos usuarios

2. **Verificar Dependencias:**
   
   * Asegurarse de tener instalados los módulos: base, crm, website

3. **Configurar Integración TicketProo (Opcional):**
   
   * Ir a Ajustes → Ajustes Generales
   * Buscar sección "TicketProo Integration"
   * Configurar URL de API (viene por defecto)
   * Ingresar Token de API
   * Guardar cambios

Uso
===

**Para Usuarios Públicos:**

1. Acceder a: ``http://tu-dominio.com/user/register``
2. Completar el formulario con:
   
   * Nombre (requerido)
   * Apellido (requerido)
   * Correo Electrónico (requerido)
   * Teléfono (opcional)
   * Empresa (opcional)
   * Cargo (opcional)
   * Mensaje (opcional)

3. Al enviar el formulario:
   
   * Se crea automáticamente un usuario interno
   * Se genera una contraseña aleatoria segura
   * Se muestra el usuario y contraseña en pantalla
   * Se crea una oportunidad en CRM con los datos

**Para Administradores:**

* Revisar nuevos usuarios en: Ajustes → Usuarios
* Revisar oportunidades creadas en: CRM → Pipeline
* Los nuevos usuarios tendrán los mismos permisos que el usuario plantilla

Funcionalidad Técnica
=====================

**Modelo res.users extendido:**

* Campo ``is_template_user``: Booleano para marcar usuario plantilla
* Método ``get_template_user()``: Obtiene el usuario marcado como plantilla
* Método ``create_user_from_form()``: Crea usuario clonando la plantilla

**Controlador Web:**

* Ruta ``/user/register``: Muestra el formulario
* Ruta ``/user/register/submit``: Procesa el formulario

**Proceso de Creación:**

1. Valida campos requeridos
2. Busca usuario plantilla configurado
3. Crea partner con datos del formulario
4. Clona grupos y permisos del usuario plantilla
5. Genera contraseña aleatoria de 12 caracteres
6. Crea oportunidad en CRM
7. Muestra credenciales al usuario

Seguridad
=========

* Las contraseñas son generadas aleatoriamente con 12 caracteres (letras y números)
* Se recomienda al usuario cambiar la contraseña después del primer login
* El formulario es accesible públicamente (auth='public')
* La creación de usuarios se ejecuta con permisos sudo

Créditos
========

Autor: Marlon Falcon
Website: https://www.marlonfalcon.com
Licencia: LGPL-3
