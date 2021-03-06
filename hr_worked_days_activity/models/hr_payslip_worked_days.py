# -*- coding:utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Savoir-faire Linux. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _


class hr_payslip_worked_days(models.Model):
    _inherit = 'hr.payslip.worked_days'

    activity_id = fields.Many2one('hr.activity', 'Activity', required=True, 
                                  default='_get_default_activity')
    
    @api.multi
    def _get_default_activity(self):
        """
        This function searches activities and return an activity.

        This is important because hr_worked_days_from_timesheet
        module's yml tests will fail otherwise because it can't create
        worked days records.

        It returns a leave type because leave types are the same for every
        employees whereas job positions are different from an employee to
        another.
        """
        activities = self.env['hr.activity'].search( [('type', '=', 'leave')])
        return activities and activities[0] or False

#     _defaults = {
#         'activity_id': lambda self, cr, uid, context=None:
#         self._get_default_activity(cr, uid, context=context)
#     }
