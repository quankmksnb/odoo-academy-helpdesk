from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    ticket_ids = fields.One2many(
        "academy.helpdesk.ticket", "partner_id", string="Tickets"
    )

    ticket_count = fields.Integer(
        string="Ticket Count", compute="_compute_ticket_count"
    )

    @api.depends("ticket_ids")
    def _compute_ticket_count(self):
        for partner in self:
            partner.ticket_count = len(partner.ticket_ids)

    def action_view_tickets(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Tickets",
            "res_model": "academy.helpdesk.ticket",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }