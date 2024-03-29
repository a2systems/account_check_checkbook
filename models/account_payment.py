from odoo import tools,fields, models, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends('payment_method_code')
    def _compute_display_checkbook_type(self):
        for rec in self:
            res = False
            if rec.payment_type == 'inbound':
                if rec.payment_method_code == 'new_third_party_checks':
                    res = True
            else:
                if rec.state == 'draft' and rec.payment_method_code in ['check_printing','existing_third_party_checks']:
                    res = True
            rec.display_checkbook_type = res


    checkbook_id = fields.Many2one('account.checkbook',string='Chequera')
    checkbook_type = fields.Selection(selection=[('physical','Fisico'),('electronic','Electronico')],
            string='Tipo de cheque')
    endosable = fields.Boolean('Endosable')
    display_checkbook_type = fields.Boolean('display_check_type',compute=_compute_display_checkbook_type,store=True)

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        for rec in self:
            if rec.check_number and rec.payment_type == 'outbound':
                if not rec.checkbook_id:
                    raise ValidationError('Por favor seleccione una chequera')
                if not rec.checkbook_id.sequence_id:
                    raise ValidationError('Chequera sin secuencia')
                seq = rec.checkbook_id.sequence_id._next()
                rec.check_number = seq
                rec.checkbook_type = rec.checkbook_id.checkbook_type
        return res
    
