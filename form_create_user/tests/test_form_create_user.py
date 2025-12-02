# -*- coding: utf-8 -*-
from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestFormCreateUser(common.TransactionCase):
    """Tests para el módulo Form Create User"""

    def setUp(self):
        super(TestFormCreateUser, self).setUp()
        
        # Crear usuario plantilla de prueba
        self.template_user = self.env['res.users'].create({
            'name': 'Template Test User',
            'login': 'template_test@example.com',
            'is_template_user': True,
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
            ])],
        })

    def test_01_get_template_user(self):
        """Verificar que se puede obtener el usuario plantilla"""
        template = self.env['res.users'].get_template_user()
        self.assertTrue(template, "Debe existir un usuario plantilla")
        self.assertEqual(template.id, self.template_user.id)
        self.assertTrue(template.is_template_user)

    def test_02_create_user_from_form(self):
        """Verificar creación de usuario desde formulario"""
        result = self.env['res.users'].create_user_from_form(
            name='Test',
            lastname='User',
            email='testuser@example.com',
            phone='+123456789',
            company='Test Company',
            position='Tester'
        )
        
        # Verificar resultado
        self.assertIn('user_id', result)
        self.assertIn('login', result)
        self.assertIn('password', result)
        self.assertIn('user_name', result)
        
        # Verificar usuario creado
        user = self.env['res.users'].browse(result['user_id'])
        self.assertEqual(user.login, 'testuser@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertFalse(user.is_template_user)
        
        # Verificar que tiene los mismos grupos que la plantilla
        self.assertEqual(
            set(user.groups_id.ids),
            set(self.template_user.groups_id.ids)
        )

    def test_03_create_user_duplicate_email(self):
        """Verificar que no se pueden crear usuarios con emails duplicados"""
        # Crear primer usuario
        self.env['res.users'].create_user_from_form(
            name='First',
            lastname='User',
            email='duplicate@example.com',
            phone='',
            company='',
            position=''
        )
        
        # Intentar crear segundo usuario con mismo email
        with self.assertRaises(ValueError) as context:
            self.env['res.users'].create_user_from_form(
                name='Second',
                lastname='User',
                email='duplicate@example.com',
                phone='',
                company='',
                position=''
            )
        
        self.assertIn('Ya existe un usuario', str(context.exception))

    def test_04_create_user_without_template(self):
        """Verificar error cuando no hay usuario plantilla"""
        # Desmarcar usuario plantilla
        self.template_user.is_template_user = False
        
        # Intentar crear usuario
        with self.assertRaises(ValueError) as context:
            self.env['res.users'].create_user_from_form(
                name='Test',
                lastname='User',
                email='notemplate@example.com',
                phone='',
                company='',
                position=''
            )
        
        self.assertIn('No se ha configurado un usuario plantilla', str(context.exception))

    def test_05_password_generation(self):
        """Verificar que las contraseñas generadas son seguras"""
        result = self.env['res.users'].create_user_from_form(
            name='Password',
            lastname='Test',
            email='passwordtest@example.com',
            phone='',
            company='',
            position=''
        )
        
        password = result['password']
        
        # Verificar longitud
        self.assertEqual(len(password), 12)
        
        # Verificar que contiene letras y números
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        self.assertTrue(has_letter, "La contraseña debe contener letras")
        self.assertTrue(has_digit, "La contraseña debe contener números")

    def test_06_partner_creation(self):
        """Verificar que se crea el partner correctamente"""
        result = self.env['res.users'].create_user_from_form(
            name='Partner',
            lastname='Test',
            email='partnertest@example.com',
            phone='+987654321',
            company='Test Corp',
            position='Manager'
        )
        
        user = self.env['res.users'].browse(result['user_id'])
        partner = user.partner_id
        
        self.assertTrue(partner, "Debe existir un partner asociado")
        self.assertEqual(partner.name, 'Partner Test')
        self.assertEqual(partner.email, 'partnertest@example.com')
        self.assertEqual(partner.phone, '+987654321')
        self.assertEqual(partner.function, 'Manager')

    def test_07_company_partner_creation(self):
        """Verificar creación de compañía como partner"""
        result = self.env['res.users'].create_user_from_form(
            name='Company',
            lastname='Test',
            email='companytest@example.com',
            phone='',
            company='Test Corporation',
            position='CEO'
        )
        
        user = self.env['res.users'].browse(result['user_id'])
        partner = user.partner_id
        
        # Verificar que tiene una compañía padre
        self.assertTrue(partner.parent_id, "Debe tener una compañía padre")
        self.assertEqual(partner.parent_id.name, 'Test Corporation')
        self.assertTrue(partner.parent_id.is_company)
