from flectra import http
from flectra.http import request
from datetime import datetime

class Ratio(http.Controller):
    @http.route('/marketing_dashboard/ratio/<year>/<qtr>/<month>/<branch_id>/<separate>', type='json')
    def get_data(self, year = None, qtr = None, month = None, branch_id = None, separate = None):
        data            =   []
        total_lead      =   0
        total_win       =   0
        total_lost      =   0
        total_opp       =   0
        alls            =   0
        crm             =   request.env['crm.lead']
        all             =   crm.search([('branch_id', '=', int(branch_id))])
        lead            =   crm.search([('branch_id', '=', int(branch_id)), ('type', '=', 'lead')])
        win             =   crm.search([('branch_id', '=', int(branch_id)), ('lost_reason', '=', None)])
        lost            =   crm.search([('branch_id', '=', int(branch_id)), ('lost_reason', '!=', None)])
        opportunity     =   crm.search([('branch_id', '=', int(branch_id)), ('type', '=', 'opportunity')])
        
        if year != None and year != 'null':
            lead            =   crm.search([('type', '=', 'lead'),
                                            ('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

            all            =   crm.search([('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

            win             =   crm.search([('lost_reason', '=', None),
                                            ('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

            lost             =   crm.search([('lost_reason', '!=', None),
                                            ('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

            opportunity      =   crm.search([('type', '=', 'opportunity'),
                                            ('branch_id', '=', int(branch_id)),
                                            ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                            ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

        if qtr != None and qtr != 'null' and year != None and year != 'null':
            if qtr == "1":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-03-01 00:00:00.000000')])
            if qtr == "2":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-06-01 00:00:00.000000')])
            if qtr == "3":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-09-01 00:00:00.000000')])
            if qtr == "4":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-12-01 00:00:00.000000')])

        if month != None and month != 'null' and year != None and year != 'null':
            if month == "1":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-02-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<=', year + '-02-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-02-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-02-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-02-01 00:00:00.000000')])

            if month == "2":
                lead            =   crm.search([('type', '=', 'lead'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

                all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

                win             =   crm.search([('lost_reason', '=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

                lost             =   crm.search([('lost_reason', '!=', None),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

                opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                ('branch_id', '=', int(branch_id)),
                                                ('create_date', '>=', year + '-02-01 00:00:00.000000'),
                                                ('create_date', '<', year + '-03-01 00:00:00.000000')])

            if month == "3":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-03-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-04-01 00:00:00.000000')])

            if month == "4":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-04-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-05-01 00:00:00.000000')])
            
            if month == "5":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-05-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-06-01 00:00:00.000000')])

            if month == "6":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-06-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-07-01 00:00:00.000000')])

            if month == "7":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-07-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-08-01 00:00:00.000000')])

            if month == "8":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-08-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-09-01 00:00:00.000000')])

            if month == "9":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-09-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-10-01 00:00:00.000000')])

            if month == "10":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-10-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-11-01 00:00:00.000000')])

            if month == "11":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-11-01 00:00:00.000000'),
                                                    ('create_date', '<', year + '-12-01 00:00:00.000000')])

            if month == "12":
                    lead            =   crm.search([('type', '=', 'lead'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

                    all            =   crm.search([('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

                    win             =   crm.search([('lost_reason', '=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

                    lost             =   crm.search([('lost_reason', '!=', None),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

                    opportunity      =   crm.search([('type', '=', 'opportunity'),
                                                    ('branch_id', '=', int(branch_id)),
                                                    ('create_date', '>=', year + '-12-01 00:00:00.000000')])

        for l in lead:
            total_lead = total_lead + l.planned_revenue

        for w in win:
            total_win = total_win + w.planned_revenue

        for lo in lost:
            total_lost = total_lost + lo.planned_revenue
        
        for o in opportunity:
            total_opp = total_opp + o.planned_revenue

        for a in all:
            alls = alls + a.planned_revenue

        bagi    =   0

        if separate == '1':
            bagi = 1000
        elif separate == '2':
            bagi = 1000000
        elif separate == '3':
            bagi = 1000000000
        
        total_lead          = total_lead // bagi
        total_win           = total_win // bagi
        total_lost          = total_lost // bagi
        total_opp           = total_opp // bagi
        alls                = alls // bagi

        data.append({
            'lead': str(len(lead)),
            'win': str(len(win)),
            'lost': str(len(lost)),
            'opportunity': str(len(opportunity)),
            'all': str(len(all)),
            'alls': alls,
            'total_lead': total_lead,
            'total_win': total_win,
            'total_lost': total_lost,
            'lost_reason': total_lost,
            'total_opportunity': total_opp,
        })

        return data