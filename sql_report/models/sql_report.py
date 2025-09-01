# -*- coding: utf-8 -*-

import csv
import base64

from odoo import api, fields, models
from odoo.exceptions import UserError

BLACKLIST = ['insert', 'update', 'delete']


class SqlReport(models.Model):
    _name = 'sql.report'
    _description = 'Reporte SQL'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(
        'Number', required=True, default='Nuevo', readonly=True)
    description = fields.Char('Description', required=True)
    select_sql = fields.Text('SQL statement', required=True, tracking=True)

    def check_select_sql(self):
        """."""
        for s in self.select_sql.split(' '):
            if s.lower() in BLACKLIST:
                raise UserError(
                    'The {} parameter is not supported.'.format(s.upper()))

    def header_csv(self, dicc):
        """."""
        return [key for key in dicc]

    def generate_report(self):
        """Generar reporte CSV desde una consulta SQL."""
        self.check_select_sql()
        try:
            # Ejecutar la consulta SQL
            self.env.cr.execute(self.select_sql)
        except Exception as e:
            raise UserError(str(e))

        if self.env.cr.rowcount:
            # Obtener los resultados de la consulta
            res = self.env.cr.dictfetchall()

            # Obtener el encabezado sin ordenar y manteniendo el orden original
            header = self.header_csv(res[0])

            # Ruta temporal para el archivo CSV
            path = '/tmp/report_sql.csv'

            # Crear y escribir el archivo CSV
            with open(path, mode='w', encoding='utf-8', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';')
                writer.writeheader()

                # Escribir las filas en el archivo CSV
                for data in res:
                    for key, val in data.items():
                        if isinstance(val, str):
                            data[key] = val.strip()
                    writer.writerow(data)

            # Leer el archivo CSV y codificarlo en base64
            with open(path, 'r', encoding='utf-8') as f:
                arch = f.read()
            data = base64.b64encode(arch.encode('utf-8'))

            # Crear el adjunto en Odoo
            attach_vals = {
                'name': 'report-sql.csv',
                'datas': data,
                'type': 'binary',
            }
            doc_id = self.env['ir.attachment'].create(attach_vals)

            # Retornar un enlace para descargar el archivo CSV
            return {
                'type': "ir.actions.act_url",
                'url': f"web/content/?model=ir.attachment&id={doc_id.id}&filename_field=datas_fname&field=datas&download=true&filename={doc_id.name}",
                'target': '_blank',
            }

        # Si no hay resultados, lanzar un error
        raise UserError('No results found')

    @api.model
    def create(self, vals):
        """."""
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sql.report') or 'Nuevo'
        return super(SqlReport, self).create(vals)
