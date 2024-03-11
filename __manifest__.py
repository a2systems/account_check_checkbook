{
    'name': 'Account Check Checkbook',
    'author':  'NTSW',
    'category': 'Sales',
    'sequence': 14,
    'summary': '',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'account',
        'l10n_latam_check',
    ],
    'data': [
             'security/ir.model.access.csv',
             'views/journal_view.xml',
             'views/payment_view.xml',
             'wizard/payment_register_view.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
