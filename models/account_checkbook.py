from odoo import tools,fields, models, api, _
from odoo.exceptions import ValidationError

class AccountCheckbook(models.Model):
    _name = "account.checkbook"
    _description = "account.checkbook"

    def unlink(self):
        raise ValidationError('No se puede borrar la chequera, marquela como inactiva por favor')

    name = fields.Char('Nombre')
    journal_id = fields.Many2one('account.journal',string='Diario')
    sequence_id = fields.Many2one('ir.sequence',string='Secuencia')
    checkbook_type = fields.Selection(selection=[('physical','Fisico'),('electronic','Electronico')],string='Tipo chequera',default='physical')
    state = fields.Selection(selection=[('active','Activo'),('inactive','Inactivo')],default='active')
