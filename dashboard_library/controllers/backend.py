# Part of Flectra. See LICENSE file for full copyright and licensing details.

from flectra import http
from flectra.http import request
from datetime import datetime


class Sprint(http.Controller):

    @http.route('/library_dashboard', type='json', auth='user')
    def start(self):

        return 'true'

    @http.route('/marketing_dashboard/branch', type='json')
    def get_data(self):
        data    =   request.env['res.branch'].search([('active', '=', 1)])
        result  =   []

        for d in data:
            result.append({
                'name': d.name,
                'id': d.id
            })

        return result