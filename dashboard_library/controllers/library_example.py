from flectra import http
from flectra.http import request
from datetime import datetime
from . import lib_function as f
from . import functions as fu

class LibraryExample(http.Controller):
    @http.route('/library_dashboard/example/<start>/<end>', type='json')
    def get_data(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/library_dashboard/example_two/<start>/<end>', type='json')
    def get_exmample(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data

    @http.route('/library_dashboard/example_pie/<start>/<end>', type='json')
    def get_exmample_pie(self, start, end):
        data    =   []
        labels  =   f.month(start, end)
        value   =   []
        crm     =   request.env['crm.lead']

        count_lead          =   crm.search([('branch_id', '=', 1),
                                    ('create_date', '>=', start),
                                    ('create_date', '<=', end)])

        count_win           =   crm.search([('lost_reason', '=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_lost          =   crm.search([('lost_reason', '!=', None),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                ('branch_id', '=', 1),
                                ('create_date', '>=', start),
                                ('create_date', '<=', end)])

        count_l  = fu.total(count_lead, 'planned_revenue')
        count_w  = fu.total(count_win, 'planned_revenue')
        count_lo = fu.total(count_lost, 'planned_revenue')
        count_o  = fu.total(count_opportunity, 'planned_revenue')

        value.append({
            'lead': count_l, 
            'win': count_w, 
            'lost': count_lo, 
            'opportunity': count_o
        })

        data.append({
            'labels': labels, 
            'value': value
        })

        return data