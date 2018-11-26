# -*- coding: utf-8 -*-

from flectra import models, fields, api
from datetime import timedelta, datetime

class project_task(models.Model):
    _inherit    =   'project.task'

    @api.model
    def update_priority(self, record):
        date_filter     =   (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        date_indo       =   (datetime.now() + timedelta(days=2)).strftime('%d-%m-%Y')

        tasks           =   self.env["project.task"].search([('date_deadline', '=', date_filter), ('progress', '<', '70')])

        for task in tasks:
            update      = task.write({ 'priority': 'm'})

            mail        = self.env["mail.activity"].create({
                'res_id': task.id,
                'res_model_id': self.env["ir.model"].search([('model', '=', 'project.task')])[0].id,
                'res_model': 'project.task',
                'activity_type_id': 1,
                'summary': 'ini summary loh',
                'note': """
                    <p><b>{}</b></p><p><b>Date Deadline {}</b></p>
                """.format(task.name, date_indo),
                'date_deadline': task.date_deadline,
                'user_id': task.user_id[0].id
            })

            