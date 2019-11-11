# Copyright 2017 Ignacio Ibeas <ignacio@acysos.com>
# Copyright 2019 Rodrigo Colombo <rcolombo@sdatos.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Hidden Fields',
    'version': '12.0.1.0.0',
    'category': 'Web',
    'author': 'Acysos S.L., '
              'Sistemas de Datos, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/web',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hidden_template_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
