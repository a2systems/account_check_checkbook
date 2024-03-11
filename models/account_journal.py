from odoo import tools,fields, models, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    checkbook_ids = fields.One2many(comodel_name='account.checkbook',inverse_name='journal_id',string='Chequeras')
    
