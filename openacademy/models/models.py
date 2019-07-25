# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class openacademy(models.Model):
    _name = 'openacademy.openacademy'

    name = fields.Char(copy=False)
    value = fields.Integer()
    description = fields.Text()
    employee_id = fields.Many2one('hr.employee', 'Employee', help="Please select employee")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('confirmed', 'Confirmed'),
        ('refused', 'Refused'),
    ], string='Statue', default='draft')
    sum_value = fields.Float('Sum Value', compute="get_sum_value", store=True)
    degree = fields.Integer('Degree')
    level = fields.Selection([
        ('failed', 'You are failed: good luck'),
        ('poor', 'You level is poor : you need hard'),
        ('good', 'You are good'),
        ('excellent', 'Excellent work'),
        ('lie', 'You are lie'),
    ], compute="get_level", store=True)
    gender = fields.Selection('Gender', related='employee_id.gender', store=True, )
    degree_2 = fields.Float()
    topics_ids = fields.One2many('topics', 'course_id', 'Topic')
    total_duration = fields.Float('Total duration', compute='get_total_duration')
    responsible_ids = fields.Many2many('hr.employee', string="Responsibles")
    is_technical = fields.Boolean('Is technical')
    type = fields.Selection([
        ('type1', 'Type1'),
        ('type2', 'Type2'),
        ('type3', 'Type3'),
    ], string='Type')

    @api.one
    @api.depends('topics_ids')
    def get_total_duration(self):
        # total = 0
        # for line in self.topics_ids:
        #     total += line.duration_hours
        # self.total_duration = total
        self.total_duration = sum([l.duration_hours for l in self.topics_ids])

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique'),
    ]

    @api.one
    @api.constrains('employee_id', 'value')
    def check_value(self):
        if self.gender == 'female':
            if self.value < 1500:
                raise ValidationError(_("Female value should be greater than 1500"))
        if self.gender == 'male':
            if self.value < 1000:
                raise ValidationError("Male value should be greater than 1000")

    @api.onchange('degree')
    def onchange_degree(self):
        self.degree_2 = self.degree * 2
        self.name = self.employee_id.gender
        self.name = False
        self.value = False
        self.employee_id = False

    @api.one
    @api.depends('degree')
    def get_level(self):
        if self.degree < 50:
            res = 'failed'
        elif self.degree < 70:
            res = 'poor'
        elif self.degree < 85:
            res = 'good'
        elif self.degree <= 100:
            res = 'excellent'
        else:
            res = "lie"
        self.level = res

    @api.one
    @api.depends('value', 'employee_id', 'employee_id.gender')
    def get_sum_value(self):
        employee_gender = self.employee_id.gender
        multiple_value = 100
        if employee_gender == 'female':
            multiple_value = 150
        self.sum_value = self.value * multiple_value

    @api.one
    def action_review(self):
        if self.value <= 5000:
            self.state = 'confirmed'
        else:
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

    @api.one
    def recalculate(self):
        type1_records = self.search([
            ('type', '=', 'type1')
        ])
        names = ''
        for rec in type1_records:
            names += ',%s' % (rec.name or '')
        self.name = names


class topics(models.Model):
    _name = "topics"

    name = fields.Char('Topic name')
    duration_hours = fields.Float('Duration (in hours)')
    course_id = fields.Many2one('Course')
