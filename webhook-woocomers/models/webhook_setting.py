from flectra import models, fields, api

class WebhookSetting(models.Model):
    _inherit                =   'res.company'
    
    woocommerce_url         =   fields.Text()
    consumer_key            =   fields.Text()
    consumer_secret         =   fields.Text()
    email_login             =   fields.Text()
    password_login          =   fields.Text()
    database                =   fields.Text()
    host                    =   fields.Text()
    branch_id               =   fields.Many2one('res.branch', string='Branch')
    team_id                 =   fields.Many2one('crm.team', string='Team')
    user_id                 =   fields.Many2one('res.users', string='User')