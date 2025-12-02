#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para la integración con TicketProo
Ejecutar desde el shell de Odoo o como script independiente
"""

def test_ticketproo_integration(env):
    """
    Prueba la integración con TicketProo enviando datos de prueba
    
    Uso desde shell de Odoo:
        from addons.form_create_user.tests import test_ticketproo
        test_ticketproo.test_ticketproo_integration(env)
    """
    
    print("=" * 70)
    print("PRUEBA DE INTEGRACIÓN TICKETPROO")
    print("=" * 70)
    
    # 1. Verificar configuración
    print("\n1. Verificando configuración...")
    integration = env['ticketproo.integration']
    config = integration.get_api_config()
    
    print(f"   URL: {config['url']}")
    print(f"   Token configurado: {'Sí' if config['token'] else 'No'}")
    
    if not config['token']:
        print("\n❌ ERROR: Token no configurado")
        print("   Configúralo en: Ajustes → Ajustes Generales → TicketProo Integration")
        return False
    
    # 2. Verificar httpx
    print("\n2. Verificando librería httpx...")
    try:
        import httpx
        print(f"   ✓ httpx instalado (versión {httpx.__version__})")
    except ImportError:
        print("   ❌ httpx NO instalado")
        print("   Instalar con: pip3 install httpx")
        return False
    
    # 3. Enviar datos de prueba
    print("\n3. Enviando datos de prueba a TicketProo...")
    
    test_data = {
        'nombre': 'Test',
        'apellido': 'Usuario',
        'email': f'test_{env.cr.dbname}@example.com',
        'telefono': '+34123456789',
        'empresa': 'Empresa Test',
        'cargo': 'Tester',
        'mensaje': 'Esto es una prueba desde Odoo',
        'utm_source': 'odoo_test',
        'utm_medium': 'sistema',
        'utm_campaign': 'prueba_integracion',
    }
    
    print(f"   Enviando: {test_data['email']}")
    
    result = integration.send_registration(test_data)
    
    # 4. Mostrar resultado
    print("\n4. Resultado:")
    if result.get('success'):
        print("   ✓ ÉXITO: Datos enviados correctamente a TicketProo")
        print(f"   Status Code: {result.get('status_code')}")
        if result.get('data'):
            print(f"   Respuesta: {result.get('data')}")
    else:
        print("   ❌ ERROR: No se pudo enviar a TicketProo")
        print(f"   Error: {result.get('error')}")
        if result.get('status_code'):
            print(f"   Status Code: {result.get('status_code')}")
    
    print("\n" + "=" * 70)
    
    return result.get('success', False)


def test_from_command_line():
    """
    Prueba independiente (sin Odoo) para verificar conectividad con TicketProo
    """
    print("=" * 70)
    print("PRUEBA INDEPENDIENTE DE TICKETPROO API")
    print("=" * 70)
    
    try:
        import httpx
        print(f"\n✓ httpx instalado (versión {httpx.__version__})")
    except ImportError:
        print("\n❌ httpx NO instalado")
        print("Instalar con: pip3 install httpx")
        return
    
    url = "https://ticketproo.com/api/landing-pages/1/submit/"
    token = "ce35e472-0579-4da4-ab1b-e051868c5ab6"
    
    payload = {
        "nombre": "Test",
        "apellido": "CLI",
        "email": "test_cli@example.com",
        "telefono": "+34999999999",
        "empresa": "Test CLI",
        "cargo": "Tester",
        "mensaje": "Prueba desde línea de comandos",
        "utm_source": "cli_test",
        "utm_medium": "terminal",
        "utm_campaign": "test"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\nEnviando a: {url}")
    print(f"Email: {payload['email']}")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload, headers=headers)
            
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code in [200, 201]:
                print("\n✓ ÉXITO: Conexión con TicketProo funcionando")
            else:
                print("\n⚠ WARNING: TicketProo respondió con error")
                
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    # Si se ejecuta directamente
    test_from_command_line()
