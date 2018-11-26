# -*- coding: utf-8 -*-
{
    'name': "webhook-woocomers",

    'description': """
        Konektor flectra dan woocommerce
    """,

    'author': "Bima Pangestu",
    'website': "http://github.com/BimaPangestu28",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base', 'sales_team', 'account', 'portal', 'base_setup', 'base_branch_company'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/webhook_views.xml',
        'views/assets.xml',
        'views/webhook_setting.xml',
        'views/webhook_log_views.xml',
    ],
    'qweb': [
        'static/src/xml/product_sync.xml',
        'static/src/xml/webhook_log.xml'
    ]
}