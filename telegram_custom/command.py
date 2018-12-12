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

    @api.model
    def meeting(self, type = None):
        users   =   self.env['res.users'].search([])
        data    =   []

        for user in users:
            option      =   [('user_id', '=', user.id)]

            if type == 'daily':
                option.append(('date', '=', (datetime.now()).strftime('%Y-%m-%d')))
            elif type == 'weekly':
                option.append(('date', '<=', (datetime.now()).strftime('%Y-%m-%d')))
                option.append(('date', '>', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')))

            timesheets  =   self.env['account.analytic.line'].search(option)
            timesheet   =   []

            for t in timesheets:
                timesheet.append({
                    'name': t.name
                })

            if len(timesheets) > 0:
                data.append({ 'name': user.name, 'timesheets': timesheet})

        return data