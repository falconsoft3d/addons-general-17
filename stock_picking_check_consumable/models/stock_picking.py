from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # campo para saber si ya generamos un albarán de salida automáticamente
    # (evitar duplicados)
    consume_out_picking_id = fields.Many2one(
        'stock.picking',
        string="Albarán de salida generado",
        readonly=True,
        copy=False
    )
    not_required_out_picking = fields.Boolean(
        compute='_compute_required_out_picking',
        default=False,
    )

    def _compute_required_out_picking(self):
        for rec in self:
            rec.not_required_out_picking = True
            if rec.state == 'done' and rec.picking_type_id.code == 'incoming' and not rec.consume_out_picking_id:
                rec.not_required_out_picking = False


    @api.model
    def _create_out_picking_for_consume(self, in_picking):
        """
        Crea y confirma un albarán de salida basado en un albarán de compra que
        tenga productos con check_consume=True.
        Retorna el nuevo picking (o None si no había productos consumibles).
        """
        # Filtramos las líneas que tengan productos consumibles
        consume_moves = in_picking.move_ids_without_package.filtered(
            lambda m: m.product_id.check_consume
        )
        if not consume_moves:
            return None

        # Obtenemos el picking_type_id de salida (por ejemplo, el primer picking type out)
        # Esto depende mucho de la configuración. Aquí hacemos un ejemplo sencillo.
        picking_type_out = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('warehouse_id', '=', in_picking.picking_type_id.warehouse_id.id),
        ], limit=1)
        if not picking_type_out:
            raise UserError(_("No se encontró un tipo de albarán de salida (outgoing) "
                              "para el almacén %s") % in_picking.picking_type_id.warehouse_id.name)

        location_dest_id = self.env['stock.location'].search([
            ('usage', '=', 'customer'),
            ('company_id', '=', in_picking.company_id.id),
        ], limit=1)

        if not location_dest_id:
            location_dest_id = self.env['stock.location'].search([
            ('usage', '=', 'customer'),
        ], limit=1)


        # Creamos el nuevo picking de salida
        out_picking_vals = {
            'picking_type_id': picking_type_out.id,
            'origin': in_picking.name,
            'location_id': picking_type_out.default_location_src_id.id,
            'location_dest_id': location_dest_id.id,
            'move_type': 'direct',  # o 'one' para forzar movimientos parciales
        }

        _logger.info("out_picking_vals: %s", out_picking_vals)

        new_out_picking = self.create(out_picking_vals)

        # Creamos los moves correspondientes
        moves_vals = []
        for move in consume_moves:
            moves_vals.append((0, 0, {
                'name': move.name,
                'product_id': move.product_id.id,
                'product_uom_qty': move.product_uom_qty,
                'product_uom': move.product_uom.id,
                'location_id': out_picking_vals['location_id'],
                'location_dest_id': out_picking_vals['location_dest_id'],
                'picking_id': new_out_picking.id,
            }))
        new_out_picking.move_ids_without_package = moves_vals

        # Guardamos referencia para no generar duplicado
        in_picking.consume_out_picking_id = new_out_picking

        # Confirmamos el albarán de salida
        new_out_picking.action_confirm()
        new_out_picking.button_validate()

        return new_out_picking

    def _action_done(self):
        """
        Sobrescribimos para crear un albarán de salida si se valida un albarán
        de compra (incoming) con productos check_consume.
        """
        res = super(StockPicking, self)._action_done()

        for picking in self:
            # solo si es un albarán de compra (incoming)
            if picking.picking_type_id.code == 'incoming':
                # y si aun no se generó uno de salida
                if not picking.consume_out_picking_id:
                    self._create_out_picking_for_consume(picking)

        return res

    def action_create_out_picking_consume(self):
        """
        Acción contextual para generar el albarán de salida en albaranes
        ya validados que no lo tengan.
        """
        for picking in self:
            if picking.state != 'done':
                raise UserError(_("El albarán %s no está validado. Primero valídalo.") % picking.name)
            if picking.picking_type_id.code != 'incoming':
                raise UserError(_("El albarán %s no es de tipo compra (incoming).") % picking.name)
            if picking.consume_out_picking_id:
                raise UserError(_("El albarán %s ya tiene un albarán de salida generado.") % picking.name)

            out_picking = self._create_out_picking_for_consume(picking)
            if out_picking:
                out_picking.action_assign()  # reservarlo automáticamente
                out_picking.action_confirm()  # confirmarlo automáticamente
            if not out_picking:
                raise UserError(_("No se creó ningún albarán de salida para el albarán %s.") % picking.name)
        return True
