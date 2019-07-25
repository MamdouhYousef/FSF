from openerp import models, fields


class Branch(models.Model):
    _name = "hr.branch"

    name = fields.Char('Branch name')
    address = fields.Text()
    po_bos = fields.Integer('PO.Box')
    open_date = fields.Date('Open date')
    close_time = fields.Datetime('Close date')
    type = fields.Selection([
        ('operation', 'Operation'),
        ('management', 'Management')
    ], string="Type")


