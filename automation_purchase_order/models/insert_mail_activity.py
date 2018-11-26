from flectra import models, fields, api
import datetime

class automation_mail_on_create_purchase(models.Model):
    _inherit    =   'mail.activity'

    @api.model
    def get_list_item(self, record):
        try:
            id_purchase_order = record.res_id
            fix_list_item = ""        
            list_item = self.env["purchase.order.line"].search([('order_id', '=', id_purchase_order)])
            for i, item in enumerate(list_item):
                fix_list_item = fix_list_item+str(int(i+1))+". "+item.name+" \t ("+str(item.product_qty)+")<br/>"
            
            
            mail_obj = self.env['mail.activity'].browse(record.id)
            mail_obj.write({
                'note': record.note+"<p><b>List Item : </b><br/>"+fix_list_item+"</p>",
            })
        except Exception as e:
            print(str(e))


