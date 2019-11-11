# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.osv import orm
import json


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    @api.multi
    def _check_hidden_field(self, model_name, field_name):
        model = self.env['ir.model'].search([('model', '=', model_name)])
        field = self.env['ir.model.fields'].search(
            [('name', '=', field_name), ('model_id', '=', model.id)])
        hidden_field = self.env['hidden.template.field'].search(
            [('field_id', '=', field.id), ('model_id', '=', model.id),
             ('company_id', '=', self.env.user.company_id.id),
             ('active', '=', True), ('readonly', '=', False)])
        if hidden_field:
            if not hidden_field.user_ids and not hidden_field.group_ids:
                return True
            if self.env.user in hidden_field.user_ids:
                return True
            for group in hidden_field.group_ids:
                if group in self.env.user.groups_id:
                    return True
        return False

    @api.multi
    def _check_readonly_field(self, model_name, field_name):
        model = self.env['ir.model'].search([('model', '=', model_name)])
        field = self.env['ir.model.fields'].search(
            [('name', '=', field_name), ('model_id', '=', model.id)])
        hidden_field = self.env['hidden.template.field'].search(
            [('field_id', '=', field.id), ('model_id', '=', model.id),
             ('company_id', '=', self.env.user.company_id.id),
             ('active', '=', True), ('readonly', '=', True)])
        if hidden_field:
            if not hidden_field.user_ids and not hidden_field.group_ids:
                return True
            if self.env.user in hidden_field.user_ids:
                return True
            for group in hidden_field.group_ids:
                if group in self.env.user.groups_id:
                    return True
        return False

    @api.multi
    def _check_safe_mode(self, node):
        modifiers = json.loads(node.get('modifiers'))
        if 'required' in modifiers and modifiers['required']:
            return True
        check_xml = 'record.' + node.get('name') + '.raw_value'
        if self.search([('arch_db', 'ilike', check_xml)]):
            return True
        return False

    @api.model
    def postprocess(self, model, node, view_id, in_tree_view, model_fields):
        fields = super(IrUiView, self).postprocess(
            model, node, view_id, in_tree_view, model_fields)
        if node.tag == 'field':
            if self._check_hidden_field(model, node.get('name')):
                modifiers = json.loads(node.get('modifiers'))
                if self._check_safe_mode(node):
                    modifiers['invisible'] = True
                    orm.transfer_modifiers_to_node(modifiers, node)
                else:
                    node.getparent().remove(node)
                    fields.pop(node.get('name'), None)
            elif self._check_readonly_field(model, node.get('name')):
                modifiers = json.loads(node.get('modifiers'))
                modifiers['readonly'] = True
                orm.transfer_modifiers_to_node(modifiers, node)
        return fields
