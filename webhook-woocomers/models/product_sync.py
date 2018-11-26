from flectra import models, fields, api

class Log(models.Model):
    _inherit    =   'product.product'
    sync        =   fields.Boolean(string="sync", default=False)
    date_sync   =   fields.Datetime()