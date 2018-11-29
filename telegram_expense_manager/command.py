# -*- coding: utf-8 -*-
from flectra import models, api
from datetime import timedelta, datetime
import re

class TelegramCommand(models.Model):
    _inherit = 'telegram.command'

    @api.model
    def get_start(self, name):
        company = self.env['res.company'].search([('name', '=', name)])[0]

        return company.start_telebot