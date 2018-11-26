{
    'name': 'Dashboard Library',
    'version': '1.0',
    'category': 'Module',
    'author': 'Bima Pangestu',
    'website': 'https://github.com/BimaPangestu28',
    'summary': 'A module for Dashboard Library',
    'depends': [
        'feremall'
    ],
    'data': [
        'views/assets.xml',
        # 'views/dashboard_views.xml',
        'views/marketing_dashboard.xml',
    ],
    'qweb': [
        'static/src/xml/library_dashboard.xml',
        'static/src/xml/marketing_dashboard.xml',
    ],
    'installable': True,
}
