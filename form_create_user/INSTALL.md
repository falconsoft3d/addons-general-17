# Guía de Instalación y Configuración Rápida

## 🚀 Instalación

1. **Reiniciar Odoo** con el módulo en el path de addons:
   ```bash
   ./odoo-bin -c odoo.conf -u form_create_user
   ```

2. **Actualizar lista de aplicaciones**:
   - Ir a Aplicaciones
   - Hacer clic en "Actualizar lista de aplicaciones"
   - Buscar "Form Create User MFH"
   - Instalar el módulo

## ⚙️ Configuración Inicial (IMPORTANTE)

### 1. Configurar Usuario Plantilla

**Este paso es OBLIGATORIO antes de usar el formulario:**

1. Ir a: `Ajustes → Usuarios y Empresas → Usuarios`
2. Seleccionar un usuario existente que tenga los permisos que quieres copiar (o crear uno nuevo)
3. Editar el usuario
4. Activar el checkbox `Usuario Plantilla`
5. Asegurarse de que el usuario tenga configurados:
   - ✅ Grupos de acceso correctos
   - ✅ Permisos necesarios
   - ✅ Compañía asignada

**Ejemplo de configuración:**
```
Usuario: Plantilla Vendedor
Grupos: Usuario interno, Ventas: Usuario
Usuario Plantilla: ☑️ Activado
```

### 2. Verificar Módulos Instalados

- ✅ Base (siempre instalado)
- ✅ CRM (instalar si no está)
- ✅ Website (instalar si no está)

## 🧪 Probar el Módulo

1. **Acceder al formulario público**:
   ```
   http://localhost:8069/user/register
   ```
   O en producción:
   ```
   https://tu-dominio.com/user/register
   ```

2. **Completar el formulario** con datos de prueba:
   - Nombre: Juan
   - Apellido: Pérez
   - Email: juan.perez@ejemplo.com
   - Teléfono: +1234567890
   - Empresa: Empresa Demo
   - Cargo: Gerente
   - Mensaje: Solicitud de acceso

3. **Verificar resultado**:
   - ✅ Se muestra usuario y contraseña generados
   - ✅ Se puede iniciar sesión con las credenciales
   - ✅ Se creó una oportunidad en CRM

## 🔍 Verificaciones

### Verificar usuario creado:
1. Ir a: `Ajustes → Usuarios`
2. Buscar: juan.perez@ejemplo.com
3. Verificar que tiene los mismos grupos que el usuario plantilla

### Verificar oportunidad creada:
1. Ir a: `CRM → Pipeline`
2. Buscar: "Registro web - Juan Pérez"
3. Verificar datos del contacto

## ⚠️ Solución de Problemas

### Error: "No se ha configurado un usuario plantilla"
**Solución**: Activar el campo "Usuario Plantilla" en un usuario existente

### Error: "Ya existe un usuario con el email..."
**Solución**: El email ya está registrado. Usar otro email o eliminar el usuario existente

### El formulario no aparece
**Solución**: 
1. Verificar que el módulo website esté instalado
2. Limpiar caché del navegador
3. Verificar la URL: `/user/register`

### Los usuarios creados no tienen permisos
**Solución**: Verificar que el usuario plantilla tenga los grupos de acceso correctos

## 📋 Checklist Pre-Producción

- [ ] Usuario plantilla configurado con permisos correctos
- [ ] Módulos base, crm y website instalados
- [ ] Formulario accesible públicamente
- [ ] Prueba de creación de usuario exitosa
- [ ] Prueba de inicio de sesión con credenciales generadas
- [ ] Oportunidad CRM creada correctamente
- [ ] Email de notificación configurado (opcional)

## 🔐 Recomendaciones de Seguridad

1. **Cambiar contraseña**: Instruir a los usuarios a cambiar su contraseña después del primer login
2. **Límite de intentos**: Considerar agregar limitación de intentos de registro
3. **Verificación de email**: Implementar verificación de email (mejora futura)
4. **Captcha**: Agregar captcha para evitar spam (mejora futura)

## 📞 Soporte

Para problemas o consultas:
- Website: https://www.marlonfalcon.com
- Revisar logs de Odoo: `var/log/odoo.log`
