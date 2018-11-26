# -*- coding: utf-8 -*-

from flectra import models, fields, api
import datetime

class automation_system(models.Model):
    _inherit    =   'purchase.order'

    def get_list_item(self, id_purchase_order):
        fix_list_item = ""        
        list_item = self.env["purchase.order.line"].search([('order_id', '=', id_purchase_order)])
        for i, item in enumerate(list_item):
            fix_list_item = fix_list_item+str(int(i+1))+". "+item.name+" \t ("+str(item.product_qty)+")<br/>"
        return fix_list_item

    def get_list_item_from_sales_order(self, id_sales_order):
        fix_list_item = ""        
        list_item = self.env["sale.order.line"].search([('order_id', '=', id_sales_order)])
        for i, item in enumerate(list_item):
            fix_list_item = fix_list_item+str(int(i+1))+". "+item.name+"<br/>"
        return fix_list_item

    @api.model
    def notify_to_purchasing(self, record):
        try:
            print("Notify to purchasing")
            # for local test
            # sales_order = self.env["sale.order"].search([('id', '=', 44)])[0]
            # id_ir_module_category = self.env['ir.module.category'].search([('name', '=', 'Purchases'),('description', '!=', '')])[0].id
            # user_ids = self.env['res.groups'].search([('category_id','=',id_ir_module_category), ('name', '=', 'Manager')])[0].users

            # for production
            # id_ir_module_category pada production server = 43
            # id_res_groups pada production server = 55
            sales_order = self.env["sale.order"].search([('name', '=', record.origin)])[0]
            user_ids = self.env['res.groups'].search([('id','=', 55)])[0].users

            order_date = datetime.datetime.strptime(sales_order.date_order, "%Y-%m-%d %H:%M:%S")
            order_date = order_date - datetime.timedelta(days=3)
            activity_type = 5

            fix_list_item = ""
            phone = record.partner_id.mobile
            summary = record.name
            link = "<a href='https://api.whatsapp.com/send?phone={phone}&text=Halo%20Admin%20Saya%20Dari%20Feremall%20Untuk%20{RFQ}%20Harap%20Segera%20Diproses.' target='_blank'>Chat Via WhatsApp</a>".format(phone=phone, RFQ=summary)
            
            fix_list_item = self.get_list_item_from_sales_order(sales_order.id)
            
            # list_item = self.env["purchase.order.line"].search([('order_id', '=', id_purchase_order)])

            # for i, item in enumerate(record.order_line):
            #     fix_list_item = fix_list_item+str(int(i+1))+". "+item.name+" \t ("+str(item.product_qty)+")<br/>"
            
            note = "<p><b>{no_rfq}</b></p><br/><p><b>Link:</b> {link}</p><br/><p><b>Phone:</b> {phone}</p><br/><p><b>List Item :</b> <br/>{list_item}</p>".format(no_rfq=summary, link=link, phone=phone, list_item=fix_list_item)
            print(fix_list_item)
            print("BBBBBBBBBBBBB")
            for user in user_ids:
                mail =self.env["mail.activity"].create({
                    'res_id': record.id,
                    'res_model_id': self.env["ir.model"].search([('model', '=', 'purchase.order')])[0].id,
                    'res_model': 'purchase.order',
                    'activity_type_id': activity_type,
                    'summary': summary,
                    'note': note,
                    'date_deadline': order_date,
                    'user_id': user.id
                })
        except Exception as e:
            print(str(e))