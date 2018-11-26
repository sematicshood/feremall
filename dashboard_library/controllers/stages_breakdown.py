from flectra import http
from flectra.http import request
from datetime import datetime
from . import functions as f

class StagesBreakdown(http.Controller):
    @http.route('/marketing_dashboard/stages_breakdown/<year>/<qtr>/<month>/<branch_id>/<separate>', type='json')
    def get_data(self, year = 2018, qtr = None, month = None, branch_id = None, separate = None):
        data            =   []
        total_lead      =   []
        total_win       =   []
        total_lost      =   []
        total_opp       =   []
        crm             =   request.env['crm.lead']

        if year == 'null':
            year = '2018'

        bulan           =   f.bulan(qtr, month, year)
        bulan_int       =   f.bulan_int(qtr, month, year)
        
        
        for ai in bulan_int:
            count_l  =   0
            count_w  =   0
            count_lo =   0
            count_o  =   0
            tm       =   str(ai)

            if ai < 12:
                tn  =   str(ai + 1)
            else:
                tn  =   str(ai)

            count_lead          =   crm.search([('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<=', year + '-' +  tn + '-01 00:00:00.000000')])

            count_win           =   crm.search([('lost_reason', '=', None),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<=', year + '-' +  tn + '-01 00:00:00.000000')])

            count_lost          =   crm.search([('lost_reason', '!=', None),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<=', year + '-' +  tn + '-01 00:00:00.000000')])

            count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<=', year + '-' +  tn + '-01 00:00:00.000000')])
            
            count_l  = f.total(count_lead, 'planned_revenue')
            count_w  = f.total(count_win, 'planned_revenue')
            count_lo = f.total(count_lost, 'planned_revenue')
            count_o  = f.total(count_opportunity, 'planned_revenue')
            
            total_lead.append(f.separate(count_l, separate))
            total_win.append(f.separate(count_w, separate))
            total_lost.append(f.separate(count_lo, separate))
            total_opp.append(f.separate(count_o, separate))
            
        data.append({
            'total_lead': total_lead,
            'total_win': total_win,
            'total_lost': total_lost,
            'total_opportunity': total_opp,
            'bulan': bulan,
        })

        return data