# -*- coding: utf-8 -*-
from flectra import http
from flectra.http import request
import requests
import json
import base64
import hmac
import hashlib
import datetime
from . import api

class ApiBca(http.Controller):
    corporate_id    =   ""

    def bca(self):
        user                 =   http.request.env.context.get('uid')
        company              =   request.env["res.users"].search([('id', '=', user)])[0].company_id[0]
        api_key              =   company.api_key
        api_secret           =   company.api_secret
        client_id            =   company.client_id
        client_secret        =   company.client_secret
        self.corporate_id    =   company.corporate_id

        bca     =   api.api_bca(api_key, api_secret, client_id, client_secret)

        return bca

    def company_id(self):
        user                 =   http.request.env.context.get('uid')
        company              =   request.env["res.users"].search([('id', '=', user)])[0].company_id[0]

        return company.id

    @http.route('/api_bca/partner_bank', type='json')
    def get_bank(self):
        bank    =   request.env["account.journal"].search([('bank_account_id', '!=', None), ('company_id', '=', self.company_id())])
        data    =   []

        for b in bank:
            data.append({
                'name': b[0].name,
                'id': bank[0].bank_account_id[0].acc_number
            })

        return data

    @http.route('/api_bca/get_balance', type='json')
    def api_balance(self):
        account_number  =   []

        bank        =   request.env["account.journal"].search([('bank_account_id', '!=', None), ('company_id', '=', self.company_id())])

        for b in bank:
            account_number.append(b.bank_account_id[0].acc_number)

        bca     =   self.bca()
        balance =   bca.get_balance(self.corporate_id, account_number or None)

        return balance["AccountDetailDataSuccess"]

    @http.route('/api_bca/get_transaction/<number>/<start>/<end>', type='json')
    def get_transaction(self, number, start, end):
        bca     =   self.bca()
        balance =   bca.account_statement(self.corporate_id, number, start, end)

        return balance