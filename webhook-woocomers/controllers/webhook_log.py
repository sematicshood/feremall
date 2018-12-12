# -*- coding: utf-8 -*-
from flectra import http
from flectra.http import request
import requests
import json

class WebhookWoocomers(http.Controller):

    @http.route('/webhook/webhook_log/get', type='json')
    def getProduct(self):
        data        =   []
        product     =   request.env["webhook.log"].search([])
        print('ganteng'*10)
        
        for p in product:
            print(p.partner_id)
            data.append({
                'user': p.user_id[0].name,
                'partner': p.partner_id[0].name if len(p.partner_id) > 0 else None,
                'product': p.product_id[0].name if len(p.product_id) > 0 else None,
                'order': p.order_id[0].name if len(p.order_id) > 0 else None,
                'description': p.description,
                'created_at': p.create_date,
            })

        return data
        