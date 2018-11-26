{
    'name': 'Dashboard Sales',
    'version': '1.0',
    'category': 'Module',
    'author': 'Sematics',
    'website': 'https://github.com/BimaPangestu28',
    'summary': 'A module for Sales Dashboard',
    'depends': [
        'feremall'
    ],
    'data': [
        'views/assets.xml',
        'views/sales_dashboard_views.xml',
    ],
    'qweb': [
        'static/src/xml/sales_dashboard.xml',
    ],
    'installable': True,
}
