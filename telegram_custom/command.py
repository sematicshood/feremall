# -*- coding: utf-8 -*-
from flectra import models, api
from datetime import timedelta, datetime
import re

class TelegramCommand(models.Model):
    _inherit = 'telegram.command'

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    @api.model
    def today_activity(self, context, type = None):
        date_next     =   (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        date_now      =   (datetime.now()).strftime('%Y-%m-%d')

        option        =    [('date_start', '>=', date_now), ('date_start', '<', date_next)]

        if type != 'all':
            option.append(('user_id', '=', context.user_id[0].id))

        projects      =   self.env['project.task'].search(option)

        data          =   []

        for p in projects:
            data.append({ 'name': p.name, 'description': self.cleanhtml(p.description), 'date_deadline': p.date_deadline, 'user': p.user_id[0].name })

        return data

    @api.model
    def due_activity(self, context, type = None):
        date_filter     =   (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        option          =   [('date_deadline', '=', date_filter)]

        if type != 'all':
            option.append(('user_id', '=', context.user_id[0].id))

        projects        =   self.env['project.task'].search(option)

        projects        =   self.env["project.task"].search(option)

        data            =   []

        for p in projects:
            data.append({ 'name': p.name, 'description': self.cleanhtml(p.description), 'date_deadline': p.date_deadline, 'user': p.user_id[0].name })

        return data