from flectra import models, fields, api

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    res_model = fields.Char(index=True)
    res_id = fields.Integer(index=True)
    public = fields.Boolean(default=True)