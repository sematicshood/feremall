from flectra import models, fields, api

class Log(models.Model):
    _name = 'webhook.log'

    user_id = fields.Many2one('res.users', string='User', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    product_id = fields.Many2one('product.product', string='Product')
    order_id = fields.Many2one('sales.order', string='Sales Order')
    description = fields.Text(string='Description', required=True)