{
    'name': 'Academy Helpdesk',
    'version': '1.0',
    'summary': 'Quan ly ticket ho tro khach hang',
    'author': 'Quan',
    'category': 'Services/Helpdesk',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/academy_helpdesk_ticket_views.xml',
        'views/academy_helpdesk_menus.xml',
    ],
    'application': True,
    'installable': True
}