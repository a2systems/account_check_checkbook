# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import frozendict


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    show_checkbook = fields.Boolean('show_checkbook',default=False)
    checkbook_id = fields.Many2one('account.checkbook',string='Chequera')
    checkbook_type = fields.Selection(selection=[('physical','Fisico'),('electronic','Electronico')],
            string='Tipo de cheque')
    endosable = fields.Boolean('Endosable')

    @api.onchange('payment_method_line_id')
    def onchange_payment_method(self):
        if self.payment_type == 'outbound' and \
            self.payment_method_line_id.payment_method_id.id == self.env.ref('account_check_printing.account_payment_method_check').id:
            self.show_checkbook = True
        else:
            self.show_checkbook = False

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        if self.checkbook_id:
            res['checkbook_id'] = self.checkbook_id.id
        if self.checkbook_type:
            res['checkbook_type'] = self.checkbook_type
        res['endosable'] = self.endosable
        return res
