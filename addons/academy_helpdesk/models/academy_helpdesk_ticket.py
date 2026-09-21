from odoo import fields, models

class AcademyHelpdeskTicket(models.Model):
    _name = "academy.helpdesk.ticket"
    _description = "Academy Helpdesk Ticket"
    _order = "create_date desc"

    name = fields.Char(string="Subject", required=True)
    ticket_ref = fields.Char(string="Ticket ID", readonly=True, copy=False, default="New")
    description = fields.Html(string="Description")
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Urgent")],
        string="Priority", default="1",
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