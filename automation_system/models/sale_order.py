# -*- coding: utf-8 -*-

from flectra import models, fields, api

class automation_system(models.Model):
    _inherit    =   'sale.order'

    def get_manager_purchase(self):
        purchase_role   =   (self.env["user.role"].search([('code', '=', 'PM')])).id
        managers        =   []
        users           =   (self.env["res.users"].search([('role_id', '=', purchase_role)]))

        for user in users:
            managers.append(user.partner_id)

        return managers

    @api.model
    def add_followers(self, record):
        managers = self.get_manager_purchase()
        
        if record.state == 'sale':
            for order in record:
                for manager in managers:
                    cek = (self.env["mail.followers"].search([('res_model', '=', 'sale.order'), ('res_id', '=', order.id), ('partner_id', '=', manager[0].id)]))
                    if len(cek) == 0:
                        order.message_subscribe([manager[0].id])
            