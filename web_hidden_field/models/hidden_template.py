# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, _


class HiddenTemplateField(models.Model):
    _name = 'hidden.template.field'
    _description = 'Hidden template field'

    field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field', required=True)
    user_ids = fields.Many2many(
        comodel_name='res.users', string='Users', relation='hidden_field_user',
        column1='hidden_field', column2='hidden_user',
        help="If you don't select any user, the field is hidden to all users")
    group_ids = fields.Many2many(
        comodel_name='res.groups', string='Groups',
        relation='hidden_field_group', column1='hidden_field',
        column2='hidden_group', help="Is you don't select any group, the field"
        "is hidden to all groups")
    active = fields.Boolean(related='template_id.active')
    model_id = fields.Many2one(
        comodel_name='ir.model', related='template_id.model_id')
    company_id = fields.Many2one(
        comodel_name='res.company', related='template_id.company_id')
    template_id = fields.Many2one(comodel_name='hidden.template')
    readonly = fields.Boolean(string="Readonly", default=False, help=_("Apply if you only want to set as a read-only field, otherwise the field will be hidden"))


class HiddenTemplate(models.Model):
    _name = 'hidden.template'
    _description = 'Hidden template'

    def _default_company(self):
        return self.env['res.company']._company_default_get('hidden.template')

    model_id = fields.Many2one(
        comodel_name='ir.model', string='Model', required=True)
    active = fields.Boolean(string="Active", default=True)
    hidden_field_id = fields.One2many(
        comodel_name='hidden.template.field', inverse_name='template_id')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', index=True,
        required=True, default=_default_company)
