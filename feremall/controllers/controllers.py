# -*- coding: utf-8 -*-
from flectra import http

# class Feremall(http.Controller):
#     @http.route('/feremall/feremall/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/feremall/feremall/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('feremall.listing', {
#             'root': '/feremall/feremall',
#             'objects': http.request.env['feremall.feremall'].search([]),
#         })

#     @http.route('/feremall/feremall/objects/<model("feremall.feremall"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('feremall.object', {
#             'object': obj
#         })