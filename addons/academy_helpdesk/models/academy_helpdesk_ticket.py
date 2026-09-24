from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError

class AcademyHelpdeskTicket(models.Model):
    _name = "academy.helpdesk.ticket"
    _description = "Academy Helpdesk Ticket"
    _order = "create_date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Subject", required=True, tracking=True)
    ticket_ref = fields.Char(string="Ticket ID", readonly=True, copy=False, default="New")
    description = fields.Html(string="Description")
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Urgent")],
        string="Priority", default="1", tracking=True
    )
    channel = fields.Selection(
        selection=[("email", "Email"), ("phone", "Phone"), ("chat", "Chat")],
        string="Channel", default="email",
    )
    customer_name = fields.Char(string="Customer Name")
    customer_email = fields.Char(string="Customer Email")
    customer_phone = fields.Char(string="Customer Phone")
    date_deadline = fields.Date(string="Deadline")
    assigned_date = fields.Datetime(string="Assigned Date")
    is_urgent = fields.Boolean(string="Urgent Flag")
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(string="Active", default=True)
    stage_id = fields.Many2one("academy.helpdesk.stage", string="Stage", tracking=True)
    days_open = fields.Integer(string="Days Open", compute="_compute_days_open")
    stage_code = fields.Char(string="Stage Code", related="stage_id.code")
    user_id = fields.Many2one("res.users", string="Assigned To", tracking=True)

    @api.depends("create_date")
    def _compute_days_open(self):
        today = fields.Date.context_today(self)
        for ticket in self:
            if ticket.create_date:
                ticket.days_open = (today - ticket.create_date.date()).days
            else:
                ticket.days_open = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("ticket_ref") or vals["ticket_ref"] == "New":
                vals["ticket_ref"] = self.env["ir.sequence"].next_by_code(
                    "academy.helpdesk.ticket"
                ) or "New"
        return super().create(vals_list)

    @api.constrains("customer_email")
    def _check_customer_email(self):
        for ticket in self:
            if ticket.customer_email and "@" not in ticket.customer_email:
                raise ValidationError(
                    "Email khách hàng phải chứa ký tự '@: %s" %ticket.customer_email
                )
    
    @api.onchange("priority")
    def _onchange_priority(self):
        for ticket in self:
            ticket.is_urgent = ticket.priority == '3'

    def action_start(self):
        self._move_to_stage("in_progress")

    def action_wait(self):
        self._move_to_stage("waiting")

    def action_customer_reply(self):
        self._move_to_stage("in_progress")

    def action_close(self):
        self._move_to_stage("closed")

    def _move_to_stage(self, code):
        stage = self.env["academy.helpdesk.stage"].search(
            [("code", "=", code)], limit=1
        )
        if not stage:
            raise UserError(
                "Chưa có tage nào với code '%s'. Vào Configuration -> Stages để tạo." %code
            )
        self.stage_id = stage.id
