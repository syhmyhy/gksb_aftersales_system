# app/filters.py

from datetime import datetime

def format_rm_currency(value):
    return f"{value:,.2f}"

def dateformat(value, format='%d-%m-%Y'):
    return value.strftime(format) if isinstance(value, datetime) else value
