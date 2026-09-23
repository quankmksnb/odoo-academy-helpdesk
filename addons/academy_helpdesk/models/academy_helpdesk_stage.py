from odoo import fields, models

class AcademyHelpdeskStage(models.Model):
    _name = "academy.helpdesk.stage"
    _description = "Helpdesk Ticket Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required = True)
    sequence = fields.Integer(string="Sequence", default=10)
    code = fields.Char(string="Code")
    fold = fields.Boolean(string="Folded in Kanban")

    _unique_code = models.Constraint(
        "unique(code)",
        "Mã stage (code) phải là duy nhất!",
    )