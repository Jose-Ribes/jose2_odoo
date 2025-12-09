# from odoo import http


# class GestionTareasJose(http.Controller):
#     @http.route('/gestion_tareas_jose/gestion_tareas_jose', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_jose/gestion_tareas_jose/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_jose.listing', {
#             'root': '/gestion_tareas_jose/gestion_tareas_jose',
#             'objects': http.request.env['gestion_tareas_jose.gestion_tareas_jose'].search([]),
#         })

#     @http.route('/gestion_tareas_jose/gestion_tareas_jose/objects/<model("gestion_tareas_jose.gestion_tareas_jose"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_jose.object', {
#             'object': obj
#         })

