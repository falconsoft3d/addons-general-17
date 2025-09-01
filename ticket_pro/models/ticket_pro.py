# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging
_logger = logging.getLogger(__name__)

class TicketPro(models.Model):
    _description = "Ticket Pro"
    _name = 'ticket.pro'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'resuelto')]

    name = fields.Char('Código', default="Nuevo", copy=False)
    title = fields.Char('Título', size=100)
    obs = fields.Text('Observación')
    obs_solucion = fields.Text('Solución')
    obs_stop = fields.Text('Stop Note')
    entry_date = fields.Datetime(
        'Fecha de Entrada', default=fields.Datetime.now)
    end_date = fields.Datetime('F. Salida')
    end_will_end = fields.Datetime('Fecha Prevista', tracking=True)
    user_id = fields.Many2one('res.users', string='Creado',
                              default=lambda self: self.env.user)

    note_id = fields.Many2one('ticket.notes', tracking=True)

    hours = fields.Integer("Horas", tracking=True)
    price = fields.Float("Precio", tracking=True)

    category_id = fields.Many2one('ticket.category', string='Categoría', tracking=True)
    ticket_id = fields.Many2one('ticket.pro', string='Relacionado', tracking=True)
    project_id = fields.Many2one('ticket.project', string='Proyecto', tracking=True)
    tproject_state_id = fields.Many2one('tproject.state', string='Etapa', tracking=True)
    sprint_id = fields.Many2one('ticket.sprint', string='Sprint', tracking=True)

    numerical_priority = fields.Integer('Prioridad #', default=1)
    documentation_state = fields.Selection([
            ('no', 'No Necesita'),
            ('25', 'Poco Documentada'),
            ('50', 'Medianamente Documentada'),
            ('100', 'Completa'),
        ],
        string='Est. Documentación', index=True, default='no',
        tracking=True,
        copy=False)

    sequence = fields.Integer('Secuencia', default=0)

    @api.depends('name','title')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "[%s] %s" % (record.name, record.title)

    #  llamar a repoerte ticket_pro_report que tiene act_ticket_pro_report
    def print_report(self):
        return self.env.ref('ticket_pro.act_ticket_pro_report').report_action(self)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        obj_tproject = self.env['tproject.state'].search([], limit=1)
        if obj_tproject:
            res['tproject_state_id'] = obj_tproject.id

        obj_category = self.env['ticket.category'].search([], limit=1)
        if obj_category:
            res['category_id'] = obj_category.id

        return res

    numero_veces = fields.Integer('# Veces', default=1)
    responsible = fields.Char('Responsable')
    advance = fields.Integer('% Avance' ,tracking=True)

    user_error_id = fields.Many2one(
        'res.users', string='Usuario', default=lambda self: self.env.user)

    user_work_id = fields.Many2one('res.users', string='Asignado', tracking=True)
    frequent_question_id = fields.Many2one('frequent.question', string='Pregunta Frecuente', tracking=True)
    video = fields.Char('Video')



    char_note = fields.Char('Notas')
    module_odoo = fields.Char('Módulo')

    comprobante_01_name = fields.Char("Adjunto")
    comprobante_01 = fields.Binary(
        string='Adjunto',
        copy=False,
        help='Adjunto')

    company_id = fields.Many2one(
        'res.company', string="Compañia", required=True,
        default=lambda self: self.env.user.company_id.id)

    type = fields.Selection([
        ('internal', 'Interno'),
        ('external', 'Público')],
        string='Tipo', index=True, default='external',
        copy=False)
    
    environment = fields.Selection([
        ('new', 'Nuevo'),
        ('dev', 'Desarrollo'),
        ('demo', 'Demo'),
        ('qa', 'Calidad'),
        ('pro', 'Producción')],
        string='Ambiente', index=True, default='new',
        tracking=True,
        copy=False)

    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('quotation', 'Cotizado'),
        ('refused', 'Rechazado'),
        ('stop', 'Espera'),
        ('aprobado', 'Aprobado'),
        ('trabajando', 'Trabajando'),
        ('actualizar', 'Actualizar'),
        ('resuelto', 'Resuelto'),
        ('calificado', 'Calificado')],
        string='Estado', index=True, readonly=True, default='borrador',
        tracking=True,
        copy=False)

    clasificacion = fields.Selection([
        ('soporte', 'Soporte'),
        ('desarrollo', 'Desarrollo')],
        string='Clasificación', index=True, default='soporte', copy=False)

    calificacion = fields.Selection([
        ('0', 'Malo'),
        ('1', 'Regular'),
        ('2', 'Bueno'),
        ('3', 'Excelente')],
        string='Calificación', default='0', copy=False)

    obs_calificacion = fields.Text('Nota Calificación')

    prioridad = fields.Selection(
        [('baja', 'Baja'),
         ('media', 'Media'),
         ('alta', 'Alta')],
        default='baja', copy=False)

    user_task_id = fields.Many2one(
        'user.task', string='U.T', compute='_compute_user_task_id', index=True)

    contract_type = fields.Selection(string='Tipo C.', selection=[('c', 'Contrato'), ('e', 'Evolutivo')], default='e')
    question_ids = fields.One2many('ticket.questions.and.answers', 'task_id', string='Preguntas y Respuestas')
    improvement_ids = fields.One2many('ticket.improvement', 'task_id', string='Mejoras')

    def _compute_user_task_id(self):
        control_line_obj = self.env['progress.control.line']
        for record in self:
            progress_control_obj = control_line_obj.search([('task_id','=',record.id)], limit=1)
            if progress_control_obj:
                record.user_task_id = progress_control_obj.progress_control_id.user_task_id.id
            else:
                record.user_task_id = False

    def exe_autorizar(self):
        for record in self:
            record.send_email_ticket('⚠️ Ticket Creado: %s' % self.name)
            record.state = 'aprobado'
            record.message_post(
                body=_("Ticket Aprobado por: %s") % record.env.user.name)

    def exe_stop(self):
        for record in self:
            record.state = 'stop'
            record.message_post(
                body=_("Ticket a Stop por: %s") % record.env.user.name)

    def exe_actualizar(self):
        for record in self:
            record.state = 'actualizar'
            record.message_post(
                body=_("Ticket a Actualizar por: %s") % record.env.user.name)

    def exe_refuse(self):
        for record in self:
            record.state = 'refused'
            record.message_post(
                body=_("Ticket a Rechazado por: %s") % record.env.user.name)

    def exe_work(self):
        for record in self:
            record.user_work_id = record.env.user
            record.state = 'trabajando'
            record.message_post(
                body=_("Iniciando el trabajo: %s") % record.env.user.name)

    def exe_quotation(self):
        for record in self:
            if record.price == 0 and record.hours == 0:
                raise UserError("Debe valorar Ticket %s para cotizarlo"%record.title)
            record.state = 'quotation'
            record.message_post(
                body=_("Ticket a Cotizado por: %s") % record.env.user.name)

    def exe_resuelto(self):
        attach_obj = self.env['ir.attachment']
        for record in self:
            record.user_work_id = record.env.user
            record.send_email_ticket('Ticket Terminado: %s' % self.name)
            record.state = 'resuelto'

    def send_email_ticket(self, subject):
        _logger.info("Send Email Ticket")
        try:
            ticket_send_email = self.env['ir.config_parameter'].sudo().get_param('ticket.send.email')
            _logger.info("ticket_send_email %s" % ticket_send_email)
        except Exception as e:
            _logger.info("Error %s" % e)
            ticket_send_email = False

        if not ticket_send_email:
            _logger.info("No se envia email")
            return

        attach_obj = self.env['ir.attachment']
        for record in self:
            if self.comprobante_01:
                attachment = attach_obj.create({
                    'name': self.comprobante_01_name,
                    'datas': self.comprobante_01,
                    'store_fname': self.comprobante_01_name,
                    'res_model': 'ticket.pro',
                    'type': 'binary'
                })
            else:
                attachment = False
            body_html = f"""
                        <table style="width: 100%; border-collapse: collapse; border: 1px solid black;">
                            <tbody>
                               <tr>
                                    <td colspan="2" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Título:&nbsp;</strong> {self.title}</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="2" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Observación:&nbsp;</strong> {self.obs}</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Compañia:&nbsp;</strong> {self.company_id.name}</p>
                                    </td>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Estado:&nbsp;</strong> {self.state}</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Prioridad:&nbsp;</strong> {self.prioridad}</p>
                                    </td>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Fecha:&nbsp;</strong> {self.entry_date}</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Usuario:&nbsp;</strong> {self.user_id.name}</p>
                                    </td>
                                    <td width="50%" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Categoria:&nbsp;</strong> {self.category_id.name}</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="2" style="border: 1px solid black; padding: 8px;">
                                        <p><strong>Solución:&nbsp;</strong> {self.obs_solucion}</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        """

            _logger.info("State %s" % self.state)

            if self.state == 'borrador':
                email_from = self.env.user.email
                email_to = self.category_id.email
            else:
                email_from = self.category_id.email
                email_to = self.env.user.email


            email = self.env['mail.mail'].create({
                'subject': subject,
                'email_from': email_from,
                'email_to': email_to,
                'body_html': body_html,
                'attachment_ids': [(6, 0, attachment.ids)] if attachment else [(5,)],
            })

            email.send()
            if email:
                self.message_post(
                    body=_("Enviado email a Soporte: %s" % self.category_id.name))
            else:
                body=_("Error al enviar email a Soporte: %s" % self.category_id.name)


    def exe_abrir(self):
        for record in self:
            record.numero_veces = record.numero_veces + 1
            record.state = 'borrador'
            record.message_post(body=_("Se Abre de nuevo: %s") %
                                record.env.user.name)


    def exe_close(self):
        if self.calificacion == '0':
            raise ValidationError(
                "Por favor califica nuestro trabajo así mejoramos con tu ayuda, muchas gracias.")
        for record in self:
            record.state = 'calificado'
            record.message_post(body=_("Calificado como: %s") %
                                record.calificacion)



    @api.model
    def retrieve_dashboard(self):
        self.env.cr.execute("""
        SELECT (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
        ) total_open,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_open_this_year,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_open_this_month,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date) - 1
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_open_last_month,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND DATE_PART('week', entry_date) = DATE_PART('week', current_date)
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_open_this_week,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND DATE_PART('week', entry_date) = DATE_PART('week', current_date) - 1
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_open_last_week,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state not in ('resuelto', 'calificado')
            AND prioridad = 'alta'
        ) total_open_high_priority,

        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
        ) total_done,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_done_this_year,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_done_this_month,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date) - 1
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_done_last_month,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND DATE_PART('week', entry_date) = DATE_PART('week', current_date)
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_done_this_week,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND DATE_PART('week', entry_date) = DATE_PART('week', current_date) - 1
            AND DATE_PART('month', entry_date) = DATE_PART('month', current_date)
            AND DATE_PART('year', entry_date) = DATE_PART('year', current_date)
        ) total_done_last_week,
        (
            SELECT count(id)
            FROM ticket_pro
            WHERE state in ('resuelto', 'calificado')
            AND prioridad = 'alta'
        ) total_done_high_priority
        """)
        return self.env.cr.dictfetchall()[0]

    @api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'ticket.pro') or "Nuevo"
        return super(TicketPro, self).create(vals)

    def exe_remote(self):
        remote_ids = self.env['ticket.server'].search([])
        if remote_ids:
            try:
                remote_ids[0].create_remote_tickets(self)
            except:
                pass

    def unlink(self):
        for record in self:
            if self.env.user.has_group('ticket_pro.ticket_pro_user_delete'):
                super(TicketPro, record).unlink()
            else:
                raise UserError("Usted no tiene permiso para borrar tickets")
        return True


class TicketQuestionsandAnswers(models.Model):
    _name = 'ticket.questions.and.answers'
    _description = 'Ticket Questions and Answers'

    task_id = fields.Many2one(
        'ticket.pro', 'Ticket', ondelete='cascade')
    question = fields.Char('Pregunta')
    answer = fields.Char('Respuesta')
    user_id = fields.Many2one(
        'res.users', string='Usuario', default=lambda self: self.env.user)
    entry_date = fields.Datetime(
        'Fecha', default=fields.Datetime.now)

class TicketImprovement(models.Model):
    _name = 'ticket.improvement'
    _description = 'Ticket Improvements'

    name = fields.Text('Nombre')
    done = fields.Boolean('Hecho')
    priority = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta')],
        string='Prioridad', index=True, default='baja',
        copy=False)
    check = fields.Boolean('Comprobado')
    levt = fields.Boolean('Levantamiento')
    task_id = fields.Many2one(
        'ticket.pro', 'Ticket', ondelete='cascade')

    comprobante_01_name = fields.Char("Adjunto")
    comprobante_01 = fields.Binary(
        string='Adjunto',
        copy=False,
        help='Adjunto')


    comprobante_02_name = fields.Char("Evidencia")
    comprobante_02 = fields.Binary(
        string='Evidencia',
        copy=False,
        help='Adjunto')


    comprobante_02_name = fields.Char("Documentación")
    comprobante_02 = fields.Binary(
        string='Adjunto',
        copy=False,
        help='Adjunto')

