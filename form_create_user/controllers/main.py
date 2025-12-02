# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class FormCreateUserController(http.Controller):

    @http.route('/', type='http', auth='public', website=True, csrf=False)
    def user_register_form(self, **kwargs):
        """Muestra el formulario de registro"""
        return request.render('form_create_user.user_register_form_template')

    @http.route('/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def user_register_submit(self, **post):
        """Procesa el formulario y crea el usuario y oportunidad"""
        try:
            # Obtener datos del formulario
            name = post.get('name', '').strip()
            lastname = post.get('lastname', '').strip()
            email = post.get('email', '').strip()
            phone = post.get('phone', '').strip()
            company = post.get('company', '').strip()
            position = post.get('position', '').strip()
            message = post.get('message', '').strip()

            # Validar campos requeridos
            if not all([name, lastname, email]):
                return request.render('form_create_user.user_register_error_template', {
                    'error_message': 'Por favor complete los campos obligatorios: Nombre, Apellido y Correo Electrónico'
                })

            # Crear el usuario usando el modelo
            user_data = request.env['res.users'].sudo().create_user_from_form(
                name=name,
                lastname=lastname,
                email=email,
                phone=phone,
                company=company,
                position=position
            )

            # Crear oportunidad en CRM
            lead_vals = {
                'name': f'Registro web - {name} {lastname}',
                'contact_name': f'{name} {lastname}',
                'email_from': email,
                'phone': phone,
                'partner_name': company if company else f'{name} {lastname}',
                'function': position,
                'description': message if message else 'Registro desde formulario web público',
                'type': 'opportunity',
                'user_id': False,  # Sin asignar inicialmente
            }

            # Si existe la compañía como partner, vincularla
            if company:
                company_partner = request.env['res.partner'].sudo().search([
                    ('name', '=', company),
                    ('is_company', '=', True)
                ], limit=1)
                if company_partner:
                    lead_vals['partner_id'] = company_partner.id

            lead = request.env['crm.lead'].sudo().create(lead_vals)

            # Enviar datos a TicketProo API
            try:
                ticketproo_data = {
                    'nombre': name,
                    'apellido': lastname,
                    'email': email,
                    'telefono': phone,
                    'empresa': company,
                    'cargo': position,
                    'mensaje': message,
                    # Capturar parámetros UTM si existen
                    'utm_source': post.get('utm_source', ''),
                    'utm_medium': post.get('utm_medium', ''),
                    'utm_campaign': post.get('utm_campaign', ''),
                }
                
                ticketproo_result = request.env['ticketproo.integration'].sudo().send_registration(ticketproo_data)
                
                if ticketproo_result.get('success'):
                    _logger.info(f"Datos enviados exitosamente a TicketProo para {email}")
                else:
                    _logger.warning(f"No se pudo enviar a TicketProo: {ticketproo_result.get('error')}")
            except Exception as e:
                # No fallar el registro si TicketProo falla
                _logger.error(f"Error al enviar a TicketProo (registro continuó): {str(e)}")

            # Mostrar credenciales al usuario
            return request.render('form_create_user.user_register_success_template', {
                'user_name': user_data['user_name'],
                'login': user_data['login'],
                'password': user_data['password'],
                'lead_id': lead.id,
            })

        except ValueError as e:
            _logger.error(f"Error de validación al crear usuario: {str(e)}")
            return request.render('form_create_user.user_register_error_template', {
                'error_message': str(e)
            })
        except Exception as e:
            _logger.error(f"Error al crear usuario desde formulario: {str(e)}")
            return request.render('form_create_user.user_register_error_template', {
                'error_message': 'Ocurrió un error al procesar su solicitud. Por favor intente nuevamente o contacte al administrador.'
            })
