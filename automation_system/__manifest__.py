# -*- coding: utf-8 -*-
{
    'name': "Automation System",

    'summary': """
        Autamtion System""",

    'description': """
        Automation System
    """,

    'author': "My Company",
    'website': "https://github.com/BimaPangestu28",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_automation', 'sale', 'project', 'feremall'],

    # always loaded
    'data': [
        # 'views/action_sale_order.xml',
        'views/project_task_automation.xml'
    ],
}