from odoo import fields, models


class As2expertPartner(models.Model):
    _name = "as2expert.partner"
    _description = "AS2Expert Partner"
    _order = "name"

    name = fields.Char(required=True)
    account_id = fields.Many2one(
        "as2expert.account", required=True, ondelete="cascade", index=True
    )
    partner_ref = fields.Char(
        string="Partner id", required=True,
        help="The partner id used by the AS2Expert API (/messages/send 'partner').",
    )
    as2_id = fields.Char(string="AS2 ID")

    _sql_constraints = [
        (
            "ref_uniq",
            "unique(account_id, partner_ref)",
            "A partner reference must be unique per account.",
        ),
    ]

    def name_get(self):
        result = []
        for partner in self:
            label = partner.name
            if partner.as2_id:
                label = "%s (%s)" % (partner.name, partner.as2_id)
            result.append((partner.id, label))
        return result
