{
    "name": "PayPal - Kenya",
    "version": "1.0.0",
    'sequence': 351,
    "category": "Accounting/Payment Providers",
    "summary": "Extends the PayPal payment provider to support Kenyan Shilling (KES) currency.",
    "description": """
                           This module extends the existing PayPal payment provider in Odoo to add support for transactions in Kenyan Shilling (KES). 
                           It ensures that businesses operating in Kenya can seamlessly process payments through PayPal without currency compatibility issues.
                       """,
    "author": "Samson Maosa",
    "website": "https://github.com/coolsam726/odoo-payment-paypal-kenya",
    "license": "LGPL-3",
    "depends": ["payment_paypal"],
    "data": [
        "views/payment_provider_views.xml"
    ],
    'assets': {},
    "installable": True,
    "application": False,
    "auto_install": False,
}
