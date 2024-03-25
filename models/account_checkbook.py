from odoo import tools,fields, models, api, _
from odoo.exceptions import ValidationError

class AccountCheckbook(models.Model):
    _name = "account.checkbook"
    _description = "account.checkbook"

    def get_next_check(self):
        self.ensure_one()
        res = 0
        checks = self.env['account.payment'].search(
                [('state','=','posted'),('checkbook_id','=',self.id),('journal_id','=',self.journal_id.id)],
                )
        if checks:
            check_number = 0
            for check in checks:
                if check.check_number.isdigit() and int(check.check_number) > check_number:
                    check_number = int(check.check_number)
            if check_number:
                if check_number >= self.next_number:
                    res = check_number + 1
                else:
                    res = self.next_number
            else:
                res = 1
        else:
            res = 1
        return res

    def unlink(self):
        raise ValidationError('No se puede borrar la chequera, marquela como inactiva por favor')

    name = fields.Char('Nombre')
    journal_id = fields.Many2one('account.journal',string='Diario')
    sequence_id = fields.Many2one('ir.sequence',string='Secuencia')
    checkbook_type = fields.Selection(selection=[('physical','Fisico'),('electronic','Electronico')],string='Tipo chequera',default='physical')
    state = fields.Selection(selection=[('active','Activo'),('inactive','Inactivo')],default='active')
    next_number = fields.Integer('Siguiente numero',default=0)
