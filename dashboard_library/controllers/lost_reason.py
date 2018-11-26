from flectra import http
from flectra.http import request
from datetime import datetime
from . import functions as f

class LostReason(http.Controller):
    @http.route('/marketing_dashboard/lost_reason/<year>/<qtr>/<month>/<branch_id>/<separate>', type='json')
    def get_data(self, year = 2018, qtr = None, month = None, branch_id = None, separate = None):
        data                =   []
        bulan               =   ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
        bulan_int           =   [1,2,3,4,5,6,7,8,9,10,11,12]
        crm                 =   request.env['crm.lead']
        team                =   request.env['crm.lost.reason'].search([])
        team_name           =   []
        team_id             =   []
        team_win            =   []

        for t in team:
            team_name.append(t.name)
            team_id.append(t.id)

        if year == 'null':
            year = '2018'

        if qtr != None and qtr != 'null' and year != None and year != 'null':
            if qtr == "1":
                bulan           =   bulan[0:3]
                bulan_int       =   bulan_int[0:3]
                tm              =   1
                tn              =   3

            if qtr == "2":
                bulan           =   bulan[3:6]
                bulan_int       =   bulan_int[3:6]
                tm              =   4
                tn              =   6

            if qtr == "3":
                bulan           =   bulan[6:9]
                bulan_int       =   bulan_int[6:9]
                tm              =   7
                tn              =   9

            if qtr == "4":
                bulan           =   bulan[9:12]
                bulan_int       =   bulan_int[9:12]
                tm              =   10
                tn              =   12

        if month != None and month != 'null' and year != None and year != 'null':
            if month == "1":
                bulan           =   bulan[0:1]
                bulan_int       =   bulan_int[0:1]
                tm              =   1
                tn              =   2

            if month == "2":
                bulan           =   bulan[1:2]
                bulan_int       =   bulan_int[1:2]
                tm              =   2
                tn              =   3

            if month == "3":
                bulan           =   bulan[2:3]
                bulan_int       =   bulan_int[2:3]
                tm              =   3
                tn              =   4

            if month == "4":
                bulan           =   bulan[3:4]
                bulan_int       =   bulan_int[3:4]
                tm              =   4
                tn              =   5
            
            if month == "5":
                bulan           =   bulan[4:5]
                bulan_int       =   bulan_int[4:5]
                tm              =   5
                tn              =   6

            if month == "6":
                bulan           =   bulan[5:6]
                bulan_int       =   bulan_int[5:6]
                tm              =   6
                tn              =   7

            if month == "7":
                bulan           =   bulan[6:7]
                bulan_int       =   bulan_int[6:7]
                tm              =   7
                tn              =   8

            if month == "8":
                bulan           =   bulan[7:8]
                bulan_int       =   bulan_int[7:8]
                tm              =   8
                tn              =   9

            if month == "9":
                bulan           =   bulan[8:9]
                bulan_int       =   bulan_int[8:9]
                tm              =   9
                tn              =   10

            if month == "10":
                bulan           =   bulan[9:10]
                bulan_int       =   bulan_int[9:10]
                tm              =   10
                tn              =   11

            if month == "11":
                bulan           =   bulan[10:11]
                bulan_int       =   bulan_int[10:11]
                tm              =   11
                tn              =   12

            if month == "12":
                bulan           =   bulan[11:12]
                bulan_int       =   bulan_int[11:12]
                tm              =   12
                tn              =   13

        for id in team_id:
            skor        =   0

            if qtr != 'null' and qtr != None:
                count_win   =   crm.search([('lost_reason', '=', id),
                                ('branch_id', '=', int(branch_id)),
                                ('create_date', '>=', year + '-' +  str(tm) + '-01 00:00:00.000000'),
                                ('create_date', '<=', year + '-' +  str(tn) + '-01 00:00:00.000000')])
            elif month != 'null' and month != None:
                if month != "12":
                    count_win   =   crm.search([('lost_reason', '=', id),
                                        ('branch_id', '=', int(branch_id)),
                                        ('create_date', '>=', year + '-' +  str(tm) + '-01 00:00:00.000000'),
                                        ('create_date', '<', year + '-' +  str(tn) + '-01 00:00:00.000000')])
                else:
                    count_win   =   crm.search([('lost_reason', '=', id),
                                        ('branch_id', '=', int(branch_id)),
                                        ('create_date', '>=', year + '-' +  str(tm) + '-01 00:00:00.000000')])
            else:
                count_win   =   crm.search([('lost_reason', '=', id),
                                    ('branch_id', '=', int(branch_id)),
                                    ('create_date', '>=', year + '-01-01 00:00:00.000000'),
                                    ('create_date', '<', str(int(year) + 1) + '-01-01 00:00:00.000000')])

            skor = len(count_win)

            team_win.append(skor)

        data.append({
            'team_win': team_win,
            'team_name': team_name
        })

        return data