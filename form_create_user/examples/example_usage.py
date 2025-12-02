# -*- coding: utf-8 -*-
"""
Ejemplos de uso del módulo Form Create User

Este archivo contiene ejemplos de cómo usar las funcionalidades del módulo
desde código Python o desde la consola de Odoo.
"""

# ==============================================================================
# EJEMPLO 1: Marcar un usuario como plantilla desde código
# ==============================================================================

def marcar_usuario_plantilla(env, user_id):
    """
    Marca un usuario como plantilla para clonar
    
    Args:
        env: Entorno de Odoo
        user_id: ID del usuario a marcar como plantilla
    """
    user = env['res.users'].browse(user_id)
    user.is_template_user = True
    return f"Usuario {user.name} marcado como plantilla"


# ==============================================================================
# EJEMPLO 2: Obtener el usuario plantilla
# ==============================================================================

def obtener_usuario_plantilla(env):
    """
    Obtiene el usuario marcado como plantilla
    
    Args:
        env: Entorno de Odoo
        
    Returns:
        res.users: Usuario plantilla o False si no existe
    """
    template_user = env['res.users'].get_template_user()
    if template_user:
        print(f"Usuario plantilla: {template_user.name}")
        print(f"Login: {template_user.login}")
        print(f"Grupos: {[g.name for g in template_user.groups_id]}")
    else:
        print("No hay usuario plantilla configurado")
    return template_user


# ==============================================================================
# EJEMPLO 3: Crear usuario programáticamente desde código
# ==============================================================================

def crear_usuario_desde_codigo(env):
    """
    Crea un usuario usando el método del modelo
    
    Args:
        env: Entorno de Odoo
    """
    try:
        result = env['res.users'].create_user_from_form(
            name='Carlos',
            lastname='González',
            email='carlos.gonzalez@ejemplo.com',
            phone='+1234567890',
            company='Empresa ABC',
            position='Director'
        )
        
        print("Usuario creado exitosamente:")
        print(f"  Nombre: {result['user_name']}")
        print(f"  Login: {result['login']}")
        print(f"  Contraseña: {result['password']}")
        print(f"  ID: {result['user_id']}")
        
        return result
    except ValueError as e:
        print(f"Error: {e}")
        return None


# ==============================================================================
# EJEMPLO 4: Crear oportunidad CRM asociada
# ==============================================================================

def crear_oportunidad_crm(env, user_data, message=''):
    """
    Crea una oportunidad en CRM para un usuario creado
    
    Args:
        env: Entorno de Odoo
        user_data: Diccionario con datos del usuario
        message: Mensaje adicional
    """
    lead_vals = {
        'name': f'Registro web - {user_data["user_name"]}',
        'contact_name': user_data['user_name'],
        'email_from': user_data['login'],
        'description': message or 'Registro desde formulario web',
        'type': 'opportunity',
    }
    
    lead = env['crm.lead'].create(lead_vals)
    print(f"Oportunidad creada: {lead.name} (ID: {lead.id})")
    return lead


# ==============================================================================
# EJEMPLO 5: Listar todos los usuarios creados desde el formulario
# ==============================================================================

def listar_usuarios_del_formulario(env):
    """
    Lista usuarios que fueron clonados del usuario plantilla
    (tienen los mismos grupos que el usuario plantilla)
    
    Args:
        env: Entorno de Odoo
    """
    template_user = env['res.users'].get_template_user()
    if not template_user:
        print("No hay usuario plantilla configurado")
        return []
    
    # Buscar usuarios con grupos similares (criterio aproximado)
    all_users = env['res.users'].search([
        ('is_template_user', '=', False),
        ('share', '=', False)  # Solo usuarios internos
    ])
    
    template_groups = set(template_user.groups_id.ids)
    similar_users = []
    
    for user in all_users:
        user_groups = set(user.groups_id.ids)
        if user_groups == template_groups:
            similar_users.append(user)
    
    print(f"\nUsuarios con los mismos grupos que '{template_user.name}':")
    for user in similar_users:
        print(f"  - {user.name} ({user.login})")
    
    return similar_users


# ==============================================================================
# SCRIPT DE EJEMPLO COMPLETO
# ==============================================================================

def ejemplo_completo(env):
    """
    Ejemplo completo del flujo de creación de usuario
    """
    print("=" * 60)
    print("EJEMPLO COMPLETO: Creación de Usuario desde Formulario")
    print("=" * 60)
    
    # 1. Verificar usuario plantilla
    print("\n1. Verificando usuario plantilla...")
    template_user = obtener_usuario_plantilla(env)
    
    if not template_user:
        print("❌ No hay usuario plantilla. Configurando uno...")
        # En caso real, deberías marcar un usuario existente
        return
    
    # 2. Crear usuario
    print("\n2. Creando nuevo usuario...")
    user_data = crear_usuario_desde_codigo(env)
    
    if not user_data:
        print("❌ No se pudo crear el usuario")
        return
    
    # 3. Crear oportunidad CRM
    print("\n3. Creando oportunidad en CRM...")
    lead = crear_oportunidad_crm(
        env, 
        user_data,
        message="Usuario registrado desde ejemplo de código"
    )
    
    # 4. Listar usuarios similares
    print("\n4. Listando usuarios con configuración similar...")
    similar_users = listar_usuarios_del_formulario(env)
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado exitosamente")
    print("=" * 60)


# ==============================================================================
# CÓMO USAR ESTOS EJEMPLOS
# ==============================================================================
"""
Para usar estos ejemplos desde la consola de Odoo:

1. Abrir shell de Odoo:
   ./odoo-bin shell -c odoo.conf -d nombre_base_datos

2. Ejecutar ejemplos:
   
   # Importar el archivo
   from addons.form_create_user.examples import example_usage
   
   # Obtener usuario plantilla
   example_usage.obtener_usuario_plantilla(env)
   
   # Crear usuario
   example_usage.crear_usuario_desde_codigo(env)
   
   # Ejecutar ejemplo completo
   example_usage.ejemplo_completo(env)

3. O ejecutar directamente:
   
   env['res.users'].get_template_user()
   
   env['res.users'].create_user_from_form(
       name='Test',
       lastname='User',
       email='test@example.com',
       phone='123456',
       company='Test Co',
       position='Tester'
   )
"""
