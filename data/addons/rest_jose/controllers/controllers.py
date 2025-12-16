# from odoo import http


# class RestJose(http.Controller):
#     @http.route('/rest_jose/rest_jose', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rest_jose/rest_jose/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rest_jose.listing', {
#             'root': '/rest_jose/rest_jose',
#             'objects': http.request.env['rest_jose.rest_jose'].search([]),
#         })

#     @http.route('/rest_jose/rest_jose/objects/<model("rest_jose.rest_jose"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rest_jose.object', {
#             'object': obj
#         })

