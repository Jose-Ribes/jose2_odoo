# HolaMundo_V2/__manifest__.py

{
    'name': 'Hola Mundo V2',
    'version': '2.0',
    'summary': 'Módulo de ejemplo Hola Mundo V2',
    'description': 'Este módulo muestra un mensaje básico en Odoo con interfaz completa.',
    'author': 'Tu Nombre',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hola_view.xml',
    ],
    'installable': True,
    'application': True,
}