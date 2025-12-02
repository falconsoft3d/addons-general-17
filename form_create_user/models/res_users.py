# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_template_user = fields.Boolean(
        string='Usuario Plantilla',
        default=False,
        help='Marcar este usuario como plantilla para clonar al crear nuevos usuarios desde el formulario público'
    )

    @api.model
    def get_template_user(self):
        """Obtiene el usuario marcado como plantilla"""
        template_user = self.search([('is_template_user', '=', True)], limit=1)
        return template_user

    @api.model
    def create_user_from_form(self, name, lastname, email, phone, company, position):
        """
        Crea un usuario interno clonando el usuario plantilla
        Returns: dict con user_id, login y password
        """
        template_user = self.get_template_user()
        
        if not template_user:
            raise ValueError('No se ha configurado un usuario plantilla. Por favor marque un usuario con "Usuario Plantilla"')
        
        # Generar login único basado en el email
        login = email.lower()
        
        # Verificar si el usuario ya existe
        existing_user = self.search([('login', '=', login)], limit=1)
        if existing_user:
            raise ValueError(f'Ya existe un usuario con el email {email}')
        
        # Generar contraseña aleatoria
        import random
        import string
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # Crear partner primero
        partner_vals = {
            'name': f"{name} {lastname}",
            'email': email,
            'phone': phone,
            'function': position,
        }
        
        if company:
            # Buscar o crear la compañía como partner
            company_partner = self.env['res.partner'].search([('name', '=', company), ('is_company', '=', True)], limit=1)
            if not company_partner:
                company_partner = self.env['res.partner'].create({
                    'name': company,
                    'is_company': True,
                })
            partner_vals['parent_id'] = company_partner.id
        
        partner = self.env['res.partner'].create(partner_vals)
        
        # Copiar configuración del usuario plantilla
        user_vals = {
            'name': f"{name} {lastname}",
            'login': login,
            'password': password,
            'partner_id': partner.id,
            'groups_id': [(6, 0, template_user.groups_id.ids)],
            'company_id': template_user.company_id.id,
            'company_ids': [(6, 0, template_user.company_ids.ids)],
        }
        
        # Crear el usuario
        new_user = self.create(user_vals)
        
        return {
            'user_id': new_user.id,
            'login': login,
            'password': password,
            'user_name': new_user.name,
        }
