from odoo import tools,fields, models, api, _
from odoo.exceptions import ValidationError

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

    def _compute_display_check_number(self):
        for rec in self:
            res = False
            if rec.state == 'posted' and rec.checkbook_id:
                res = True
            rec.display_check_number = res


    checkbook_id = fields.Many2one('account.checkbook',string='Chequera')
    checkbook_type = fields.Selection(selection=[('physical','Fisico'),('electronic','Electronico')],
            string='Tipo de cheque')
    endosable = fields.Boolean('Endosable')
    display_checkbook_type = fields.Boolean('display_check_type',compute=_compute_display_checkbook_type,store=True)
    display_check_number = fields.Boolean('display_check_number',compute=_compute_display_check_number)

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        for rec in self:
            if rec.check_number and rec.payment_type == 'outbound':
                if not rec.checkbook_id:
                    raise ValidationError('Por favor seleccione una chequera')
                #seq = rec.checkbook_id.sequence_id._next()
                seq = rec.checkbook_id.get_next_check()
                rec.check_number = seq
                rec.checkbook_type = rec.checkbook_id.checkbook_type
                checkbook_id = rec.checkbook_id
                checkbook_id.next_number = seq
        return res
    
