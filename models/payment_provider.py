import json

from odoo import models, fields, api, _
from .. import const
class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    paypal_base_currency_id = fields.Many2one(
        'res.currency',
        string="PayPal Base Currency",
        help="The currency in which amounts are sent to PayPal. "
             "It must be a currency supported by PayPal.",
        required_if_provider='paypal',
        default=lambda self: self.env.ref('base.USD'),
    )

    def _get_supported_currencies(self):
        """ Extend the supported currencies to include KES for PayPal provider. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'paypal':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies

    def _paypal_get_inline_form_values(self, currency=None):
        inline_form_values = {
            'provider_id': self.id,
            'client_id': self.paypal_client_id,
            'currency_code': currency and currency.name,
        }
        if currency and currency.name == 'KES':
            inline_form_values['currency_code'] = self.paypal_base_currency_id.name
            inline_form_values['converted_amount'] = currency._convert(
                self.env.context.get('amount', 0.0),
                self.paypal_base_currency_id,
                self.env.company,
                fields.Date.today()
            )
        return json.dumps(inline_form_values)