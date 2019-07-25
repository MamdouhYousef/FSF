from openerp import models, fields, api


class cars(models.Model):
    _name = 'new.car'

    plat_number = fields.Char('Plat number')
    model = fields.Integer('Model')
    purchase_date = fields.Date('Purchase date')
    type_id = fields.Many2one('type.of.car', 'Type')
    desc = fields.Html('Description')
    image = fields.Binary('Image')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('confirmed', 'Confirmed'),
        ('refused', 'Refused'),
    ], string='Statue', default='draft')

    @api.one
    def action_review(self):
        self.state = 'reviewed'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_refuse(self):
        self.state = 'refused'

    @api.one
    def action_reset(self):
        self.state = 'draft'

class type_of_car(models.Model):
    _name = "type.of.car"

    name = fields.Char('Type name', required=True)
