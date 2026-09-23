{
    'name': 'Academy Helpdesk',
    'version': '1.0',
    'summary': 'Quan ly ticket ho tro khach hang',
    'author': 'Quan',
    'category': 'Services/Helpdesk',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/academy_helpdesk_demo.xml',
        'views/academy_helpdesk_ticket_views.xml',
        'views/academy_helpdesk_stage_view.xml',
        'views/academy_helpdesk_menus.xml',
        
    ],
    'application': True,
    'installable': True
}