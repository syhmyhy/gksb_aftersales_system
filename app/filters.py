# app/filters.py

import locale

def format_rm_currency(value):
    # Set the locale to Malaysian Ringgit (Bahasa Malaysia)
    locale.setlocale(locale.LC_ALL, 'ms_MY.UTF-8')  # Set locale to Malaysian Ringgit (Bahasa Malaysia)
    return locale.currency(value, grouping=True, symbol='RM')
