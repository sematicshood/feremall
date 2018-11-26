# Part of Flectra. See LICENSE file for full copyright and licensing details.

from flectra import http
from flectra.http import request
from datetime import datetime


class Sprint(http.Controller):

    @http.route('/operational_dashboard', type='json', auth='user')
    def start(self, **param):
        print('='*10)
        print(param.get('month'))
        option  =   []

        if param.get('project') == 'active':
            option.append(('active', '=', True))

        if param.get('year') != None:
            if param.get('month') == None or param.get('month') == 'undefined':
                year    =   int(param.get('year'))
                next_y  =   year + 1
                option.append(('create_date', '>=', '{}-1-1'.format(year)))
                option.append(('create_date', '<', '{}-1-1'.format(next_y)))
            elif param.get('month') != 'undefined':
                year    =   int(param.get('year'))
                next_y  =   year + 1
                month   =   int(param.get('month'))
                next_m  =   month + 1

                option.append(('create_date', '>=', '{}-{}-1'.format(year, month)))
                
                if month == 12:
                    option.append(('create_date', '<', '{}-1-1'.format(next_y)))
                else:
                    option.append(('create_date', '<', '{}-{}-1'.format(year, next_m)))

        print(option)

        projects    = request.env['project.project'].search(option)

        data        = []

        for project in projects:
            if param.get('project') == 'active':
                tasks = request.env["project.task"].search([('project_id', '=', project.id), ('date_end', '!=', False), ('active', '=', True)])
            else:
                tasks = request.env["project.task"].search([('project_id', '=', project.id), ('date_end', '!=', False)])
                
            task_all    = []

            for task in tasks:
                task_all.append({ 'id': task.id, 'parent_id': project.id, 'name': task.name, 'start': task.date_start, 'end': task.date_end, 'bobot': task.planned_hours, 'bobot_undone': task.remaining_hours, 'bobot_done': task.effective_hours, 'team': task.user_id[0].name if len(task.user_id) > 0 else None, 'percent': task.progress })

            data.append({'id': project.id, 'name': project.name, 'series': task_all })

        return data