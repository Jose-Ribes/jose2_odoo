# from odoo import http


# class GestionRestauranteJose(http.Controller):
#     @http.route('/gestion_restaurante_jose/gestion_restaurante_jose', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_jose/gestion_restaurante_jose/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_jose.listing', {
#             'root': '/gestion_restaurante_jose/gestion_restaurante_jose',
#             'objects': http.request.env['gestion_restaurante_jose.gestion_restaurante_jose'].search([]),
#         })

#     @http.route('/gestion_restaurante_jose/gestion_restaurante_jose/objects/<model("gestion_restaurante_jose.gestion_restaurante_jose"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_jose.object', {
#             'object': obj
#         })

