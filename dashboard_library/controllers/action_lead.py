from flectra import http
from flectra.http import request
from datetime import datetime

class ActionLead(http.Controller):
    @http.route('/marketing_dashboard/action_lead/<year>/<qtr>/<month>/<branch_id>', type='json')
    def get_data(self, year = None, qtr = None, month = None, branch_id = None):
        data            =   []
        crm             =   request.env['crm.lead']
        lead            =   crm.search([('branch_id', '=', int(branch_id))])
        
        if year != None and year != 'null':
            lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

        if qtr != None and qtr != 'null' and year != None and year != 'null':
            if qtr == "1":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

            if qtr == "2":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])

            if qtr == "3":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])

            if qtr == "4":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

        if month != None and month != 'null' and year != None and year != 'null':
            if month == "1":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-02-01 00:00:00.000000')])

            if month == "2":
                lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

            if month == "3":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

            if month == "4":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])
            
            if month == "5":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

            if month == "6":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

            if month == "7":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

            if month == "8":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

            if month == "9":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

            if month == "10":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

            if month == "11":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

            if month == "12":
                    lead            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

        for l in lead:
            data.append({
                'name': l.name,
                'team': l.team_id.name,
                'tgl_lead': l.date_open,
                'umur_lead': l.day_open,
                'lead_clode': l.day_close,
                'tgl_update_tahapan': l.date_last_stage_update,
                'tgl_konversi_terakhir': l.date_conversion,
                'dateline': l.date_deadline,
                'tgl_action_terakhir': l.date_action_last
            })

        return data