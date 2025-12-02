# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

try:
    import httpx
except ImportError:
    _logger.warning("El módulo 'httpx' no está instalado. La integración con TicketProo no funcionará. Instalar con: pip install httpx")
    httpx = None


class TicketProoIntegration(models.TransientModel):
    _name = 'ticketproo.integration'
    _description = 'Integración con TicketProo API'

    @api.model
    def get_api_config(self):
        """Obtiene la configuración de la API desde parámetros del sistema"""
        ICP = self.env['ir.config_parameter'].sudo()
        return {
            'url': ICP.get_param('ticketproo.api.url', 'https://ticketproo.com/api/landing-pages/1/submit/'),
            'token': ICP.get_param('ticketproo.api.token', ''),
        }

    @api.model
    def send_registration(self, data):
        """
        Envía los datos de registro a TicketProo API
        
        Args:
            data: Diccionario con los datos del registro (nombre, apellido, email, etc.)
            
        Returns:
            dict: Respuesta de la API o dict con error
        """
        if not httpx:
            _logger.error("httpx no está instalado. No se puede enviar datos a TicketProo.")
            return {'success': False, 'error': 'httpx module not installed'}

        config = self.get_api_config()
        api_url = config['url']
        api_token = config['token']

        if not api_token:
            _logger.warning("Token de TicketProo no configurado. No se enviarán datos.")
            return {'success': False, 'error': 'API token not configured'}

        # Preparar payload
        payload = {
            'nombre': data.get('nombre', ''),
            'apellido': data.get('apellido', ''),
            'email': data.get('email', ''),
            'telefono': data.get('telefono', ''),
            'empresa': data.get('empresa', ''),
            'cargo': data.get('cargo', ''),
            'mensaje': data.get('mensaje', ''),
        }

        # Agregar parámetros UTM si existen
        if data.get('utm_source'):
            payload['utm_source'] = data['utm_source']
        if data.get('utm_medium'):
            payload['utm_medium'] = data['utm_medium']
        if data.get('utm_campaign'):
            payload['utm_campaign'] = data['utm_campaign']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_token}'
        }

        try:
            _logger.info(f"Enviando registro a TicketProo: {payload.get('email')}")
            
            with httpx.Client(timeout=10.0) as client:
                response = client.post(api_url, json=payload, headers=headers)
                
                _logger.info(f"Respuesta de TicketProo - Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    result = response.json() if response.text else {}
                    _logger.info(f"Registro enviado exitosamente a TicketProo: {result}")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'data': result
                    }
                else:
                    error_msg = f"Error en API TicketProo: {response.status_code} - {response.text}"
                    _logger.error(error_msg)
                    return {
                        'success': False,
                        'status_code': response.status_code,
                        'error': response.text
                    }

        except httpx.TimeoutException as e:
            error_msg = f"Timeout al conectar con TicketProo: {str(e)}"
            _logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except httpx.RequestError as e:
            error_msg = f"Error de conexión con TicketProo: {str(e)}"
            _logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Error inesperado al enviar a TicketProo: {str(e)}"
            _logger.error(error_msg)
            return {'success': False, 'error': error_msg}
