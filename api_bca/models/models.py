# -*- coding: utf-8 -*-

from flectra import models, fields, api

class api_bca(models.Model):
    _inherit = 'res.company'

    api_key = fields.Text()
    api_secret = fields.Text()
    client_id = fields.Text()
    client_secret = fields.Text()
    corporate_id = fields.Text()