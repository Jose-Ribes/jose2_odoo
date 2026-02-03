# from odoo import http


# class DronifyJose(http.Controller):
#     @http.route('/dronify_jose/dronify_jose', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dronify_jose/dronify_jose/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dronify_jose.listing', {
#             'root': '/dronify_jose/dronify_jose',
#             'objects': http.request.env['dronify_jose.dronify_jose'].search([]),
#         })

#     @http.route('/dronify_jose/dronify_jose/objects/<model("dronify_jose.dronify_jose"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dronify_jose.object', {
#             'object': obj
#         })

