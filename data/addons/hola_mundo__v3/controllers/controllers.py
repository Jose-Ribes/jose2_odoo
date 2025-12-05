# from odoo import http


# class HolaMundoV3(http.Controller):
#     @http.route('/hola_mundo__v3/hola_mundo__v3', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hola_mundo__v3/hola_mundo__v3/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hola_mundo__v3.listing', {
#             'root': '/hola_mundo__v3/hola_mundo__v3',
#             'objects': http.request.env['hola_mundo__v3.hola_mundo__v3'].search([]),
#         })

#     @http.route('/hola_mundo__v3/hola_mundo__v3/objects/<model("hola_mundo__v3.hola_mundo__v3"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hola_mundo__v3.object', {
#             'object': obj
#         })

