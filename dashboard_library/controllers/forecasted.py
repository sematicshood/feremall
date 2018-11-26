from flectra import http
from flectra.http import request
from datetime import datetime

class Forecasted(http.Controller):
    @http.route('/marketing_dashboard/forecasted/<year>/<qtr>/<month>/<branch_id>/<separate>', type='json')
    def get_data(self, year = 2018, qtr = None, month = None, branch_id = None, separate = None):
        data                =   []
        total_forecasted    =   0
        forecasted          =   []
        bulan               =   ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        bulan_int           =   [1,2,3,4,5,6,7,8,9,10,11,12]
        crm                 =   request.env['crm.lead']

        if year == 'null':
            year = '2018'

        if qtr != None and qtr != 'null' and year != None and year != 'null':
            if qtr == "1":
                bulan           =   bulan[0:3]
                bulan_int       =   bulan_int[0:3]

            if qtr == "2":
                bulan           =   bulan[3:6]
                bulan_int       =   bulan_int[3:6]

            if qtr == "3":
                bulan           =   bulan[6:9]
                bulan_int       =   bulan_int[6:9]

            if qtr == "4":
                bulan           =   bulan[9:12]
                bulan_int       =   bulan_int[9:12]

        if month != None and month != 'null' and year != None and year != 'null':
            if month == "1":
                bulan           =   bulan[0:1]
                bulan_int       =   bulan_int[0:1]

            if month == "2":
                bulan           =   bulan[1:2]
                bulan_int       =   bulan_int[1:2]

            if month == "3":
                    bulan           =   bulan[2:3]
                    bulan_int       =   bulan_int[2:3]

            if month == "4":
                    bulan           =   bulan[3:4]
                    bulan_int       =   bulan_int[3:4]
            
            if month == "5":
                    bulan           =   bulan[4:5]
                    bulan_int       =   bulan_int[4:5]

            if month == "6":
                    bulan           =   bulan[5:6]
                    bulan_int       =   bulan_int[5:6]

            if month == "7":
                    bulan           =   bulan[6:7]
                    bulan_int       =   bulan_int[6:7]

            if month == "8":
                    bulan           =   bulan[7:8]
                    bulan_int       =   bulan_int[7:8]

            if month == "9":
                    bulan           =   bulan[8:9]
                    bulan_int       =   bulan_int[8:9]

            if month == "10":
                    bulan           =   bulan[9:10]
                    bulan_int       =   bulan_int[9:10]

            if month == "11":
                    bulan           =   bulan[10:11]
                    bulan_int       =   bulan_int[10:11]

            if month == "12":
                    bulan           =   bulan[11:12]
                    bulan_int       =   bulan_int[11:12]

        for ai in bulan_int:
            tm       =   str(ai)

            if ai < 12:
                tn  =   str(ai + 1)
            else:
                tn  =   str(ai)

            if ai < 12:
                count_win           =   crm.search([('lost_reason', '=', None),
                                        ('branch_id', '=', int(branch_id)),
                                        ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                        ('create_date', '<', year + '-' +  tn + '-01 00:00:00.000000')])
                count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<', year + '-' +  tn + '-01 00:00:00.000000')])
            else:
                count_win           =   crm.search([('lost_reason', '=', None),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<', year + '-' +  tn + '-01 00:00:00.000000')])
                count_opportunity   =   crm.search([('type', '=', 'opportunity'),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-' +  tm + '-01 00:00:00.000000'),
                                    ('create_date', '<', year + '-' +  tn + '-31 00:00:00.000000')])
            
            for c in count_win:
                total_forecasted += c.planned_revenue

            for cou in count_opportunity:
                total_forecasted += cou.planned_revenue

        bagi    =   0

        if separate == '1':
            bagi = 1000
        elif separate == '2':
            bagi = 1000000
        elif separate == '3':
            bagi = 1000000000
        
        forecasted.append(total_forecasted // bagi)

        data.append({
            'forecasted': forecasted
        })

        return data