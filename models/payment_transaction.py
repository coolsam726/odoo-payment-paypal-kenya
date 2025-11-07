from odoo import models, fields, api, _
from odoo.addons.payment.logging import get_payment_logger

_logger = get_payment_logger(__name__)
class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    # def _extract_amount_data(self, payment_data):
    #     """Override of payment to extract the amount and currency from the payment data. If currency is KES convert it to paypal_base_currency_id"""
    #     if self.provider_code != 'paypal':
    #         return super()._extract_amount_data(payment_data)
    #
    #     amount_data = payment_data.get('amount', {})
    #     amount = amount_data.get('value')
    #     currency_code = amount_data.get('currency_code')
    #     # Convert KES to paypal_base_currency_id
    #     if currency_code == 'KES':
    #         base_currency = self.provider_id.paypal_base_currency_id
    #         kes_currency = self.env.ref('base.KES')
    #         amount = kes_currency._convert(float(amount), base_currency, self.company_id, fields.Date.today())
    #         currency_code = base_currency.name
    #     return {
    #         'amount': float(amount),
    #         'currency_code': currency_code,
    #     }

    def _paypal_prepare_order_payload(self):
        """Override to set the currency to paypal_base_currency_id if original currency is KES"""
        payload = super()._paypal_prepare_order_payload()
        if self.currency_id.name == 'KES':
            base_currency = self.provider_id.paypal_base_currency_id
            payload['purchase_units'][0]['amount']['currency_code'] = base_currency.name
            amount = self.currency_id._convert(self.amount, base_currency, self.company_id, fields.Date.today())
            payload['purchase_units'][0]['amount']['value'] = f"{amount:.2f}"
            # Update the current amount and currency to match the payload
            self.amount = float(amount)
            self.currency_id = base_currency
        return payload

    def _apply_updates(self, payment_data):
        if self.provider_code != 'paypal':
            return super()._apply_updates(payment_data)

        _logger.info("Applying payment transaction updates: %s", payment_data)
        if self.currency_id.name == 'KES':
            # Update payment data to reflect the original KES amount and currency
            base_currency = self.provider_id.paypal_base_currency_id
            kes_currency = self.env.ref('base.KES')
            amount_data = payment_data.get('amount', {})
            amount = amount_data.get('value')
            amount_in_kes = base_currency._convert(float(amount), kes_currency, self.company_id, fields.Date.today())
            payment_data['amount']['value'] = f"{amount_in_kes:.2f}"
            payment_data['amount']['currency_code'] = 'KES'
        return super()._apply_updates(payment_data)