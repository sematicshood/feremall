from flectra import http
from flectra.http import request
import requests
import json
from woocommerce import API
from urllib.parse import urlencode
import socket
import datetime
import sys

class ProductSync(http.Controller):
    def slugify(self, s):
        s = s.lower()

        for c in [' ', '-', '.', '/']:
            s = s.replace(c, '_')

        # s = re.sub('\W', '', s)
        s = s.replace('_', ' ')
        # s = re.sub('\s+', ' ', s)
        s = s.strip()
        s = s.replace(' ', '-')

        return s

    def company(self, getter):
        user                 =   http.request.env.context.get('uid')
        company              =   request.env["res.users"].search([('id', '=', user)])[0].company_id[0]

        if getter == 'url':
            return company.woocommerce_url
        elif getter == 'key':
            return company.consumer_key
        elif getter == 'secret':
            return company.consumer_secret


    def wp(self):
        wcapi = API(
            url                 =   self.company('url'),
            consumer_key        =   self.company('key'),
            consumer_secret     =   self.company('secret'),
            wp_api              =   True,
            version             =   "wc/v3",
            query_string_auth   =   True,
            timeout             =   None
        )

        return wcapi

    def post_log(self, user, product = None, type = 'create'):
        vals = {
            'user_id': user,
            'create_uid': user,
            'write_uid': user,
        }

        if product != None:
            vals['product_id']          =   product
            vals['description']         =   "{} {} sync".format(type, 'product')

        return request.env["webhook.log"].sudo().create(vals)

    @http.route('/webhook/product_sync/get', type='json')
    def getProduct(self):
        data        =   []
        product     =   request.env["product.product"].search([])
        
        for p in product:
            data.append({
                'id': p.id,
                'name': p.name,
                'code': p.default_code,
                'price': p.list_price,
                'category': p.categ_id[0].name,
                'sync': p.sync,
                'date_sync': p.date_sync,
                'write_date': p.product_tmpl_id[0].write_date,
            })

        return data

    @http.route('/webhook/product_sync/sync/<id>', type='json')
    def sync_product(self, id):
        #  + datetime.timedelta(minutes = 1)
        product     =   request.env["product.product"].search([("id", "=", id)])
        product.write({
            'date_sync': datetime.datetime.now(),
            'sync': True
        })
        wcapi       =   self.wp()
        
        wp_product  =   wcapi.get("products?slug={}".format(self.slugify(product[0].name))).json()

        category    =   wcapi.get("products/categories?slug={}".format(self.slugify(product[0].categ_id[0].name))).json()

        if len(category) == 0:
            category_data = {
                "name": product[0].categ_id[0].name,
            }

            category    =   wcapi.post("products/categories", category_data).json()
            
            if len(category) == 3:
                category    =   category["data"]["resource_id"]
            else:
                category    =   category["id"]
        else:
            category    =   category[0]["id"]

        images  =   request.env["ir.attachment"].search([('res_id', '=', product[0].product_tmpl_id[0].id), ('res_model', '=', 'product.template')])
        
        if len(images) > 0:
            image   =   "https://apps.feremall.com/web/binary/image?model=ir.attachment&field=datas&id=" + str(images[0].id).strip('')
            
            data = {
                "name": product[0].name,
                "type": "simple",
                "regular_price": str(product[0].list_price),
                "description": str(product[0].description),
                "categories": [
                    {
                        "id": category,
                    },
                ],
                "images": [
                    {
                        "src": image
                    },
                ]
            }
        else:
            data = {
                "name": product[0].name,
                "type": "simple",
                "regular_price": str(product[0].list_price),
                "description": str(product[0].description),
                "categories": [
                    {
                        "id": category,
                    },
                ],
            }

        if len(wp_product) > 0:
            pro  =   wcapi.put("products/{}".format(wp_product[0]["id"]), data).json()
            
            self.post_log(http.request.env.context.get('uid'), id, "update")
        else:
            pro  =   wcapi.post("products", data).json()

            self.post_log(http.request.env.context.get('uid'), id, "create")
        
        return pro