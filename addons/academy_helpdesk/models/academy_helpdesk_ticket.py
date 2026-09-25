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
    partner_id = fields.Many2one("res.partner", string="Customer", tracking=True)
    customer_name = fields.Char(string="Customer Name")
    customer_email = fields.Char(string="Customer Email")
    customer_phone = fields.Char(string="Customer Phone")
    date_deadline = fields.Date(string="Deadline")
    assigned_date = fields.Datetime(string="Assigned Date")
    date_closed = fields.Datetime(string="Closed Date", readonly=True)
    is_urgent = fields.Boolean(
        string="Urgent Flag", compute="_compute_is_urgent", store=True
    )
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(string="Active", default=True)
    stage_id = fields.Many2one("academy.helpdesk.stage", string="Stage", tracking=True,
    default=lambda self: self.env["academy.helpdesk.stage"].search(
            [("code", "=", "new")], limit=1
        ),
    )
    days_open = fields.Integer(string="Days Open", compute="_compute_days_open")
    stage_code = fields.Char(string="Stage Code", related="stage_id.code")
    user_id = fields.Many2one("res.users", string="Assigned To", tracking=True)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        for ticker in self:
            if ticker.partner_id:
                ticker.customer_name = ticker.partner_id.name
                ticker.customer_email = ticker.partner_id.email
                ticker.customer_phone = ticker.partner_id.phone

    @api.depends("create_date", "date_closed")
    def _compute_days_open(self):
        today = fields.Date.context_today(self)
        for ticket in self:
            if not ticket.create_date:
                ticket.days_open = 0
                continue
            end = ticket.date_closed.date() if ticket.date_closed else today
            ticket.days_open = (end - ticket.create_date.date()).days

    @api.depends("priority")
    def _compute_is_urgent(self):
        for ticket in self:
            ticket.is_urgent = ticket.priority == "3"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("ticket_ref") or vals["ticket_ref"] == "New":
                vals["ticket_ref"] = self.env["ir.sequence"].next_by_code(
                    "academy.helpdesk.ticket"
                ) or "New"
            if vals.get("user_id") and not vals.get("assigned_date"):
                vals["assigned_date"] = fields.Datetime.now()
            if vals.get("stage_id"):
                stage = self.env["academy.helpdesk.stage"].browse(vals["stage_id"])
                if stage.code == "closed" and not vals.get("date_closed"):
                    vals["date_closed"] = fields.Datetime.now()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("user_id"):
            vals["assigned_date"] = fields.Datetime.now()
        if vals.get("stage_id"):
            stage = self.env["academy.helpdesk.stage"].browse(vals["stage_id"])
            vals["date_closed"] = fields.Datetime.now() if stage.code == "closed" else False
        return super().write(vals)

    @api.constrains("customer_email")
    def _check_customer_email(self):
        for ticket in self:
            if ticket.customer_email and "@" not in ticket.customer_email:
                raise ValidationError(
                    "Email khách hàng phải chứa ký tự '@': %s" %ticket.customer_email
                )
    
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
                "Chưa có stage nào với code '%s'. Vào Configuration -> Stages để tạo." %code
            )
        self.stage_id = stage.id
