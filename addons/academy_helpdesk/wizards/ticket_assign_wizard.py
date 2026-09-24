from odoo import api, fields, models
from odoo.exceptions import UserError

class AcademyTicketAssignWizard(models.TransientModel):
    _name = "academy.ticket.assign.wizard"
    _description = "Wizard gán agent cho ticket hàng loạt"

    user_id = fields.Many2one("res.users", string="Assign To", required=True)
    ticket_ids = fields.Many2many("academy.helpdesk.ticket", string="Tickets")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get("active_ids", [])
        if active_ids:
            res["ticket_ids"] = [(6, 0, active_ids)]
        return res

    def action_assign(self):
        self.ensure_one()
        if not self.ticket_ids:
            raise UserError("Chưa chọn ticket nào để gán.")
        self.ticket_ids.write({"user_id": self.user_id.id})
        return {"type": "ir.actions.act_window_close"}