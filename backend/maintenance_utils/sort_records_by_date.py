# maintenance_utils/sort_records_by_date.py
from datetime import datetime

def sort_records_by_date(records, date_field):
    """
    Sorts a list of records by a specified date field in ascending order.
    
    :param records: List of dictionaries containing records
    :param date_field: The key in the dictionaries that contains the date to sort by
    :return: List of dictionaries sorted by the specified date field
    """
    # Ensure the date_field exists in the records
    if not records or date_field not in records[0]:
        return records  # Return as is if no records or date_field doesn't exist

    return sorted(records, key=lambda x: datetime.strptime(x[date_field], "%Y-%m-%d"))
