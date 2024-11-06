from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_next_service_date(last_service_date, service_interval_months):
    """
    Calculates the next service date based on the last service date and service interval.
    
    :param last_service_date: Date of the last service as a string (e.g., 'YYYY-MM-DD')
    :param service_interval_months: Number of months until the next service is due
    :return: Calculated next service date as a string in 'YYYY-MM-DD' format
    """
    last_service = datetime.strptime(last_service_date, "%Y-%m-%d")
    next_service_due = last_service + relativedelta(months=service_interval_months)
    return next_service_due.strftime("%Y-%m-%d")
