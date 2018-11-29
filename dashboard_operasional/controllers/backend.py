# Part of Flectra. See LICENSE file for full copyright and licensing details.

from flectra import http
from flectra.http import request
from datetime import datetime
from datetime import timedelta, datetime

class Sprint(http.Controller):
    def option(self, param, custom = None, type = None):
        option      =   []
        print('='*20)
        id_user     =   http.request.env.context.get('uid')
        manager     =   request.env['res.groups'].search([('name','=','Manager'), ('category_id.name', '=', 'Project')])
        is_manager  =   False

        for t in manager.users:
            if t.id == id_user:
                is_manager = True

        if param.get('users') == False or param.get('users') == None or param.get('users') == '':
            if type == 'project':
                if param.get('project') != None and param.get('project') != 'active':
                    option.append(('id', '=', int(param.get('project'))))
            elif type == 'task':
                if param.get('project') != None and param.get('project') != 'active':
                    option.append(('project_id.id', '=', int(param.get('project'))))

            if is_manager == False:
                option.append(('user_id', '=', id_user))
        else:
            option.append(('user_id', '=', int(param.get('users'))))

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
        elif param.get('start') != None and param.get('end') != None:
            if param.get('start') != param.get('end'):
                option.append(('create_date', '>=', param.get('start')))
                option.append(('create_date', '<=', param.get('end')))
            else:
                option.append(('create_date', '=', param.get('start')))

        if custom != None:
            for c in custom:
                option.append(c)

        return option

    @http.route('/operational_dashboard/cek_manager', type='json', auth='user')    
    def cek_m(self):
        id_user     =   http.request.env.context.get('uid')
        manager     =   request.env['res.groups'].search([('name','=','Manager'), ('category_id.name', '=', 'Project')])
        is_manager  =   False

        for t in manager.users:
            if t.id == id_user:
                is_manager = True

        if is_manager == False:
            return False
        else:
            users   =   request.env['res.users'].search([])
            data    =   []

            for user in users:
                data.append({ 'id': user.id, 'nama': user.name })

            return data

    @http.route('/library_dashboard/task-proyek', type='json', auth='user')    
    def task(self, **param):
        option          =   self.option(param, type = 'task')
        data            =   []
        t_done          =   0
        t_undone        =   0
        t_total         =   0

        t_done          =   request.env['account.analytic.line'].search_count(self.option(param, [('unit_amount', '>', 0)], type = 'task'))

        t_undone        =   request.env['account.analytic.line'].search_count(self.option(param, [('unit_amount', '=', 0)], type = 'task'))

        t_total         =   request.env['account.analytic.line'].search_count(option)

        labels = ['selesai', 'belum selesai']
        value  = [{ 'selesai': t_done, 'belum selesai': t_undone }]

        data.append({
            'labels': labels, 
            'value': value,
            'total': t_total
        })

        return data

    @http.route('/operational_dashboard/projects', type='json', auth='user')
    def project(self, **param):
        option      =   self.option(param)
        data        =   []
        print(option)

        projects    =   request.env['project.project'].search(option)
        print(projects)

        for project in projects:
            data.append({ 'name': project[0].name, 'id': project[0].id })

        return data

    @http.route('/operational_dashboard', type='json', auth='user')
    def start(self, **param):
        callb       =   {}
        count_total =   []

        option      =   self.option(param, type = 'project')

        projects    =   request.env['project.project'].search(option)

        data        =   []

        for project in projects:
            if param.get('project') == 'active':
                tasks = request.env["project.task"].search([('project_id', '=', project.id), ('date_deadline', '!=', False), ('active', '=', True)])
            else:
                tasks = request.env["project.task"].search([('project_id', '=', project.id), ('date_deadline', '!=', False)])
                
            task_all    = []

            for task in tasks:
                timesheet_all   =   []

                timesheets      =   request.env['account.analytic.line'].search([('task_id', '=', task.id)])

                for timesheet in timesheets:
                    timesheet_all.append({
                        'id': timesheet.id, 
                        'parent_id': task.id, 
                        'name': timesheet.name, 
                        'start': timesheet.date, 
                        'end': task.date_deadline, 
                        'bobot': '-', 
                        'bobot_undone': '-', 
                        'bobot_done': timesheet.unit_amount, 
                        'team': timesheet.user_id[0].name if len(timesheet.user_id) > 0 else None, 
                        'percent': 100 if timesheet.unit_amount > 0 else 0,    
                    })

                task_all.append({ 
                    'id': task.id, 
                    'parent_id': project.id, 
                    'name': task.name, 
                    'start': task.date_start, 
                    'end': task.date_deadline, 
                    'bobot': task.planned_hours, 
                    'bobot_undone': task.remaining_hours, 
                    'bobot_done': task.effective_hours, 
                    'team': task.user_id[0].name if len(task.user_id) > 0 else None, 
                    'percent': task.progress,
                    'timesheets': timesheet_all
                })

                
                data.append({'id': project.id, 'name': project.name, 'series': task_all })

        callb['project'] = data

        return callb