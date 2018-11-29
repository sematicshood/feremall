# -*- coding: utf-8 -*-

from flectra import models, fields, api

class api_bca(models.Model):
    _inherit = 'res.company'

    start_telebot = fields.Text()