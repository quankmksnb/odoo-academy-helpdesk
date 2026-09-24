from odoo import http
from odoo.http import request

class AcademyHelpdeskController(http.Controller):

    @http.route(
        "/academy/helpdesk/ticket/<int:ticket_id>/summary",
        type="jsonrpc", auth="user", methods=["POST"],
    )
    def ticket_summary(self, ticket_id):
        ticket = request.env["academy.helpdesk.ticket"].browse(ticket_id)
        ticket.check_access("read")
        return {
            "ref": ticket.ticket_ref,
            "subject": ticket.name,
            "customer": ticket.customer_name,
            "stage": ticket.stage_id.name or "",
            "priority": ticket.priority,
            "assigned_to": ticket.user_id.name or "",
        }