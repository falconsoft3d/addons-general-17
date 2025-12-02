#!/bin/bash
# =============================================================================
# COMANDOS ÚTILES PARA EL MÓDULO FORM_CREATE_USER
# =============================================================================

# -----------------------------------------------------------------------------
# INSTALACIÓN Y ACTUALIZACIÓN
# -----------------------------------------------------------------------------

# Instalar el módulo por primera vez
./odoo-bin -c odoo.conf -d nombre_db -i form_create_user

# Actualizar el módulo después de cambios
./odoo-bin -c odoo.conf -d nombre_db -u form_create_user

# Instalar con modo desarrollo
./odoo-bin -c odoo.conf -d nombre_db -i form_create_user --dev=all

# Actualizar y ver logs detallados
./odoo-bin -c odoo.conf -d nombre_db -u form_create_user --log-level=debug

# -----------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------

# Ejecutar todos los tests del módulo
./odoo-bin -c odoo.conf -d nombre_db -u form_create_user --test-enable --log-level=test

# Ejecutar tests específicos
./odoo-bin -c odoo.conf -d nombre_db --test-enable --log-level=test \
  --test-tags form_create_user

# Ejecutar tests con cobertura (requiere coverage)
coverage run --source=addons/form_create_user ./odoo-bin -c odoo.conf -d nombre_db \
  --test-enable --log-level=test --stop-after-init
coverage report
coverage html

# -----------------------------------------------------------------------------
# DESARROLLO
# -----------------------------------------------------------------------------

# Iniciar Odoo en modo desarrollo con recarga automática
./odoo-bin -c odoo.conf -d nombre_db --dev=all

# Ver logs en tiempo real (en otra terminal)
tail -f /var/log/odoo/odoo.log

# Verificar sintaxis Python de todos los archivos
find . -name "*.py" -exec python3 -m py_compile {} \;

# Buscar errores comunes con pylint
pylint models/res_users.py
pylint controllers/main.py

# Formatear código con black
black models/ controllers/

# -----------------------------------------------------------------------------
# BASE DE DATOS
# -----------------------------------------------------------------------------

# Crear una base de datos de prueba
createdb -U odoo test_form_create_user

# Inicializar base de datos con el módulo
./odoo-bin -c odoo.conf -d test_form_create_user -i form_create_user --stop-after-init

# Hacer backup de la base de datos
pg_dump -U odoo test_form_create_user > backup_form_create_user.sql

# Restaurar backup
psql -U odoo test_form_create_user < backup_form_create_user.sql

# Borrar base de datos de prueba
dropdb -U odoo test_form_create_user

# -----------------------------------------------------------------------------
# SHELL/CONSOLA INTERACTIVA
# -----------------------------------------------------------------------------

# Abrir shell de Odoo
./odoo-bin shell -c odoo.conf -d nombre_db

# Comandos útiles dentro del shell:
# >>> env['res.users'].get_template_user()
# >>> env['res.users'].create_user_from_form(name='Test', lastname='User', email='test@example.com', phone='', company='', position='')
# >>> env['crm.lead'].search([('name', 'like', 'Registro web')])
# >>> env['res.users'].search([('is_template_user', '=', True)])

# -----------------------------------------------------------------------------
# DEPURACIÓN
# -----------------------------------------------------------------------------

# Ver usuarios creados recientemente
echo "SELECT id, name, login, create_date FROM res_users ORDER BY create_date DESC LIMIT 10;" | psql -U odoo nombre_db

# Ver oportunidades CRM recientes
echo "SELECT id, name, contact_name, email_from, create_date FROM crm_lead WHERE name LIKE '%Registro web%' ORDER BY create_date DESC;" | psql -U odoo nombre_db

# Ver usuario plantilla
echo "SELECT id, name, login FROM res_users WHERE is_template_user = true;" | psql -U odoo nombre_db

# Limpiar datos de prueba
echo "DELETE FROM res_users WHERE login LIKE '%@example.com' AND id > 2;" | psql -U odoo nombre_db
echo "DELETE FROM crm_lead WHERE name LIKE '%Registro web%';" | psql -U odoo nombre_db

# -----------------------------------------------------------------------------
# PRODUCCIÓN
# -----------------------------------------------------------------------------

# Instalar en producción con modo worker
./odoo-bin -c odoo.conf -d nombre_db -i form_create_user --workers=4

# Actualizar en producción sin downtime (usando staging)
# 1. Crear copia de la base de datos
pg_dump -U odoo produccion_db | psql -U odoo staging_db

# 2. Probar actualización en staging
./odoo-bin -c odoo-staging.conf -d staging_db -u form_create_user --stop-after-init

# 3. Si todo está OK, actualizar producción en horario de bajo tráfico
./odoo-bin -c odoo.conf -d produccion_db -u form_create_user --stop-after-init

# Reiniciar Odoo en producción (systemd)
sudo systemctl restart odoo

# Ver logs de producción
sudo journalctl -u odoo -f

# -----------------------------------------------------------------------------
# VERIFICACIONES
# -----------------------------------------------------------------------------

# Verificar que el módulo está instalado
echo "SELECT name, state FROM ir_module_module WHERE name = 'form_create_user';" | psql -U odoo nombre_db

# Verificar dependencias instaladas
echo "SELECT name, state FROM ir_module_module WHERE name IN ('base', 'crm', 'website');" | psql -U odoo nombre_db

# Verificar tablas creadas
echo "\dt" | psql -U odoo nombre_db | grep res_users

# Verificar permisos del directorio
ls -la /path/to/odoo/addons/form_create_user/

# -----------------------------------------------------------------------------
# TROUBLESHOOTING
# -----------------------------------------------------------------------------

# Ver errores recientes en logs
tail -100 /var/log/odoo/odoo.log | grep ERROR

# Ver warnings recientes
tail -100 /var/log/odoo/odoo.log | grep WARNING

# Buscar errores específicos del módulo
grep "form_create_user" /var/log/odoo/odoo.log | grep ERROR

# Limpiar assets (si hay problemas con CSS)
./odoo-bin -c odoo.conf -d nombre_db --dev=all

# O desde la interfaz: Ajustes → Técnico → Base de Datos → Regenerar Assets

# Verificar que las rutas web están registradas
echo "SELECT route FROM ir_http WHERE route LIKE '%user/register%';" | psql -U odoo nombre_db

# -----------------------------------------------------------------------------
# DOCUMENTACIÓN
# -----------------------------------------------------------------------------

# Generar documentación con Sphinx (si está instalado)
sphinx-build -b html docs/ docs/_build/

# Ver README en formato HTML
rst2html.py README.rst > README.html
open README.html

# -----------------------------------------------------------------------------
# GIT (Control de versiones)
# -----------------------------------------------------------------------------

# Inicializar repositorio
git init
git add .
git commit -m "Initial commit: Form Create User module for Odoo 17"

# Ignorar archivos innecesarios
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.swp
*.swo
*~
.DS_Store
*.log
EOF

# Crear tag de versión
git tag -a v1.0 -m "Version 1.0 - Initial release"

# -----------------------------------------------------------------------------
# ÚTILES
# -----------------------------------------------------------------------------

# Contar líneas de código
find . -name "*.py" -exec wc -l {} + | tail -1

# Ver estructura de archivos
find . -type f | grep -v __pycache__ | sort

# Buscar TODOs en el código
grep -r "TODO\|FIXME\|XXX" --include="*.py" .

# Verificar enlaces en README
grep -o 'http[s]*://[^"]*' README.rst

# =============================================================================
# NOTAS
# =============================================================================

# - Reemplazar "nombre_db" con el nombre real de tu base de datos
# - Reemplazar rutas según tu instalación de Odoo
# - Ajustar usuario PostgreSQL según tu configuración (default: odoo)
# - Verificar rutas de logs según tu sistema operativo

# =============================================================================
